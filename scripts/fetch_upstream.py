"""Fetch pinned owner source for audit tests; all downloads stay Git-ignored."""
from pathlib import Path
from urllib.request import Request, urlopen
import io
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ASD_SHA = 'f699dc7b7af5726df5d8e79161d192eac22cfafb'
MMA_SHA = 'f632b7e56291805ac6d4debc8c7421b0d2c48f2e'
FORK_FILES = {
    'mmaction_asdmotion.py': 'configs/skeleton/posec3d/asdmotion.py',
    'mmaction_augmentations.py': 'mmaction/datasets/pipelines/augmentations.py',
    'mmaction_pose_loading.py': 'mmaction/datasets/pipelines/pose_loading.py',
    'mmaction_pose_dataset.py': 'mmaction/datasets/pose_dataset.py',
    'mmaction_loading.py': 'mmaction/datasets/pipelines/loading.py',
    'mmaction_formatting.py': 'mmaction/datasets/pipelines/formatting.py',
    'mmaction_compose.py': 'mmaction/datasets/pipelines/compose.py',
    'mmaction___init__.py': 'mmaction/datasets/pipelines/__init__.py',
}


def fetch(url):
    with urlopen(Request(url, headers={'User-Agent': 'ASDMotion-research-source-audit'}), timeout=90) as response:
        return response.read()


def main():
    target = ROOT / 'external/ASDMotion-main'
    if not (target / 'README.md').exists():
        archive = fetch(f'https://codeload.github.com/Dinstein-Lab/ASDMotion/zip/{ASD_SHA}')
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            for entry in z.infolist():
                relative = Path(*Path(entry.filename).parts[1:])
                destination = (target / relative).resolve()
                if not destination.is_relative_to(target.resolve()):
                    raise ValueError('Archive path outside target')
                if entry.is_dir() or not relative.parts:
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                if not destination.exists():
                    destination.write_bytes(z.read(entry))
    for local_name, upstream_path in FORK_FILES.items():
        destination = ROOT / 'references/source_snapshots' / local_name
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(fetch(f'https://raw.githubusercontent.com/TalBarami/mmaction2/{MMA_SHA}/{upstream_path}'))
    print('Pinned source available locally. No dataset or weights downloaded.')


if __name__ == '__main__':
    main()
