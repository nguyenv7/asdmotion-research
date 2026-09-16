import sys, unittest, pickle, io
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from asdmotion_research.temporal import aggregate_windows,extract_events,interval_iou
from asdmotion_research.io import NumpyUnpickler

class ResearchTests(unittest.TestCase):
    def test_frame_zero_terminal_and_singleton_events(self):
        self.assertEqual(extract_events(np.array([.9,0,.9,.9])),[(0,1),(2,4)])
    def test_uncovered_is_missing(self):
        score,cov=aggregate_windows([0,1],[2,3],[.2,.9],4)
        np.testing.assert_allclose(score[:3],[.2,.9,.9]); self.assertTrue(np.isnan(score[3]))
        self.assertEqual(cov.tolist(),[1,2,1,0])
    def test_mean_and_max_differ(self):
        score,_=aggregate_windows([0,1],[2,3],[.2,.9],3,'mean')
        self.assertAlmostEqual(score[1],.55)
    def test_half_open_iou(self):
        self.assertEqual(interval_iou((0,2),(2,4)),0)
        self.assertAlmostEqual(interval_iou((0,3),(1,4)),.5)
    def test_restricted_numpy_roundtrip(self):
        obj=NumpyUnpickler(io.BytesIO(pickle.dumps(np.array([1.,2.]),protocol=4))).load()
        np.testing.assert_equal(obj,[1.,2.])
    def test_reject_other_global(self):
        import pathlib
        with self.assertRaises(pickle.UnpicklingError):
            NumpyUnpickler(io.BytesIO(pickle.dumps(pathlib.Path('x')))).load()

if __name__=='__main__': unittest.main()
