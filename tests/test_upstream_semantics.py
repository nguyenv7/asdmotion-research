"""Executable counterexamples for pinned upstream; passing means issue reproduced.

Run: .venv/Scripts/python.exe -m unittest discover -s tests -p test_upstream_semantics.py -v
AST extraction runs actual upstream function bodies without importing CUDA/MMCV.
No upstream file is modified. These are characterization tests, not fixes.
"""
import ast
import os
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / 'external/ASDMotion-main/src/asdmotion'
FORK = ROOT / 'references/source_snapshots/mmaction_pose_loading.py'


def extracted(file, names, **extra):
    tree = ast.parse(Path(file).read_text(encoding='utf-8'))
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    for n in nodes:
        n.decorator_list = []
        if isinstance(n, ast.ClassDef):
            n.bases = []
    ns = {'np': np, 'pd': pd, 'path': os.path, 'osp': os.path,
          'tqdm': lambda x, **kwargs: x, **extra}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(file), 'exec'), ns)
    return ns


def skeleton(t):
    return {'keypoint': np.zeros((1, t, 17, 2)),
            'keypoint_score': np.zeros((1, t, 17)), 'frame_dir': 'example',
            'child_ids': np.zeros(t), 'child_detected': np.ones(t)}


COLS = ['video', 'video_full_name', 'video_path', 'start_time', 'end_time',
        'start_frame', 'end_frame', 'movement', 'calc_date', 'annotator', 'stereotypical_score']


def rows(intervals):
    return pd.DataFrame([['v', 'v.mp4', 'v.mp4', s/30, e/30, s, e,
                         movement, 'today', 'model', score]
                         for s, e, movement, score in intervals], columns=COLS)


class UpstreamCounterexamples(unittest.TestCase):
    def test_aggregation_undefined_name(self):
        ns = extracted(UP/'pipeline/aggregator.py', ['aggregate', 'unify'])
        with self.assertRaisesRegex(NameError, 'NET_NAME'):
            ns['aggregate'](rows([(0, 200, '', .9)]), .85)

    def test_threshold_equality_excluded(self):
        ns = extracted(UP/'pipeline/aggregator.py', ['aggregate', 'unify'], NET_NAME='test')
        out = ns['aggregate'](rows([(0, 200, '', .85)]), .85)
        self.assertEqual(out.iloc[0]['movement'], 'NoAction')

    def test_final_positive_run_not_merged(self):
        ns = extracted(UP/'pipeline/aggregator.py', ['aggregate', 'unify'], NET_NAME='test')
        out = ns['aggregate'](rows([(0, 200, '', .9), (30, 230, '', .1), (60, 260, '', .9)]), .85)
        # Correct positive union is [0,260), one event. Upstream returns two
        # overlapping positives and an intervening negative-length NoAction row.
        self.assertEqual(sum(out.movement == 'Stereotypical'), 2)
        self.assertTrue(((out.end_frame-out.start_frame) < 0).any())

    def test_window_short_video_and_tail(self):
        cls = extracted(UP/'pipeline/splitter.py', ['Splitter'])['Splitter']
        self.assertEqual(cls(skeleton(59), 200, 30, 60).intervals, [])
        self.assertEqual(cls(skeleton(200), 200, 30, 60).intervals[-1], (120, 200))
        self.assertEqual(cls(skeleton(201), 200, 30, 60).intervals[0], (0, 200))

    def test_missing_child_selects_last_person(self):
        cls = extracted(FORK, ['ChildDetect'])['ChildDetect']
        sample = {'child_ids': np.array([-1]), 'keypoint': np.array([[[[11., 12.]]], [[[91., 92.]]]]),
                  'keypoint_score': np.ones((2, 1, 1))}
        out = cls()(sample)
        np.testing.assert_array_equal(out['keypoint'][0, 0, 0], [91, 92])

    def test_converter_requires_unproduced_adjust(self):
        ns = extracted(UP/'pipeline/openpose_executor.py', ['OpenposeInitializer'],
                       BODY_25_LAYOUT=None, COCO_LAYOUT=None,
                       SkeletonSource=SimpleNamespace(VIDEO='video', IMAGE='image'))
        instance = ns['OpenposeInitializer'].__new__(ns['OpenposeInitializer'])
        instance._to_posec3d_numpy = lambda *args: (np.zeros((1, 1, 17, 2)), np.zeros((1, 1, 17)))
        raw = dict(data=[{}], name='v', video_path='v', resolution=(1920,1080), fps=30,
                   length_seconds=1, frame_count=30)
        with self.assertRaisesRegex(KeyError, 'adjust'):
            instance.to_poseC3D(raw)

    def test_no_smm_conclusion_omits_zero_row(self):
        cls = extracted(UP/'detector/detector.py', ['Predictor'])['Predictor']
        instance = cls.__new__(cls)
        info = {'properties': {'fps':30, 'length':10, 'frame_count':300,
                               'valid_frames':300, 'last_valid_frame':299}}
        out = instance.conclude(rows([(0,300,'NoAction',.1)]), info)
        self.assertEqual(len(out), 0)

    def test_duration_can_exceed_valid_denominator(self):
        cls = extracted(UP/'detector/detector.py', ['Predictor'])['Predictor']
        instance = cls.__new__(cls)
        info = {'properties': {'fps':30, 'length':10, 'frame_count':300,
                               'valid_frames':100, 'last_valid_frame':299}}
        out = instance.conclude(rows([(0,300,'Stereotypical',.9)]), info)
        self.assertEqual(out.iloc[0]['smm_proportion'], 3.0)

    def test_interpolation_selects_farther_reference(self):
        tree = ast.parse((UP/'child_detector/skeleton_matcher.py').read_text())
        expr = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'j' for t in n.targets))
        chosen = eval(compile(ast.Expression(expr), '<upstream j>', 'eval'), {'prev': 1, 'next': 9, 'i': 2})
        self.assertEqual(chosen, 9)  # 7 frames away rather than 1.

    def test_test_pipeline_randomly_crops_long_clips(self):
        ns = {}
        exec((ROOT/'references/source_snapshots/mmaction_asdmotion.py').read_text(), ns)
        self.assertIn('Splitter', [x['type'] for x in ns['test_pipeline']])
        file = ROOT/'references/source_snapshots/mmaction_augmentations.py'
        first = extracted(file, ['Splitter'], random=SimpleNamespace(randint=lambda a,b: a))['Splitter']
        last = extracted(file, ['Splitter'], random=SimpleNamespace(randint=lambda a,b: b))['Splitter']
        sample = skeleton(300)
        sample['keypoint'][0, :, 0, 0] = np.arange(300)
        a, b = first(200)(sample.copy()), last(200)(sample.copy())
        self.assertEqual(a['keypoint'][0,0,0,0], 0)
        self.assertEqual(b['keypoint'][0,0,0,0], 100)


if __name__ == '__main__':
    unittest.main()
