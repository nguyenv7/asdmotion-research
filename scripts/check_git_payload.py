"""Reject data/model files and large blobs in the Git index before publishing."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_DATA = {'data/README.md', 'data/raw/README.md', 'data/raw/manifest.json'}
BLOCKED_SUFFIXES = {'.pkl', '.pickle', '.pth', '.pt', '.npy', '.npz', '.parquet', '.h5', '.hdf5', '.zip', '.tar', '.gz', '.mp4', '.mov', '.avi'}


def main():
    entries = subprocess.check_output(['git', 'ls-files', '-s', '-z'], cwd=ROOT).split(b'\0')
    errors = []; sizes = []
    for entry in entries:
        if not entry:
            continue
        header, raw_path = entry.split(b'\t', 1)
        path = raw_path.decode('utf-8'); sha = header.split()[1].decode()
        size = int(subprocess.check_output(['git', 'cat-file', '-s', sha], cwd=ROOT))
        sizes.append((size, path))
        if path.startswith('data/') and path not in ALLOWED_DATA:
            errors.append(f'Dataset/derived data in Git: {path}')
        if Path(path).suffix.lower() in BLOCKED_SUFFIXES:
            errors.append(f'Excluded binary type in Git: {path}')
        if path.startswith(('.venv/', 'external/', 'tmp/', 'images-from-papers/', 'references/source_snapshots/')):
            errors.append(f'Local-only directory in Git: {path}')
        if path.startswith('references/papers/') and Path(path).suffix.lower() in {'.pdf', '.txt'}:
            errors.append(f'Downloaded paper in Git: {path}')
        if size > 1_000_000:
            errors.append(f'Blob exceeds 1 MB: {path} ({size} bytes)')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(sizes)} files; {sum(s for s, _ in sizes):,} bytes; no dataset/model blobs; every file below 1 MB.')
    for size, path in sorted(sizes, reverse=True)[:5]:
        print(f'{size:>9,}  {path}')


if __name__ == '__main__':
    main()
