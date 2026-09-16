"""Fetch public paper PDFs and record successes/failures; run from repository root."""
from pathlib import Path
from urllib.request import Request, urlopen
import json, hashlib, concurrent.futures

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'mbaye2026_persistent_homology.pdf': 'https://www.nature.com/articles/s41598-026-60095-8.pdf',
    'paulo2025_move4as.pdf': 'https://publikationen.bibliothek.kit.edu/1000188491/170761564',
    'zhang2025_apmfnet_author_manuscript.pdf': 'https://baiqiaozhang.cc/assets/files/JBHI_revision.pdf',
    'freud2025_grasping.pdf': 'https://esgeo3.weebly.com/uploads/8/8/2/1/88213736/freud2025kinematics.pdf',
    'amraee2026_vlm.pdf': 'https://openaccess.thecvf.com/content/CVPR2026W/CV4Smalls/papers/Amraee_Toward_Automated_Behavior_Understanding_in_Autism_A_Zero-Shot_Vision-Language_Model_CVPRW_2026_paper.pdf',
    'lemler2025_multilabel.pdf': 'https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/aur.70020',
    'koehler2024_synchrony.pdf': 'https://www.nature.com/articles/s41598-024-56098-y.pdf',
    'manelisbaram2025_facial.pdf': 'https://link.springer.com/content/pdf/10.1186/s13229-025-00685-x.pdf',
}

def fetch(item):
    filename, url = item
    row = {'file': filename, 'url': url, 'retrieved': '2026-09-16'}
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (research literature download)'})
        with urlopen(req, timeout=30) as response:
            data = response.read()
        if not data.startswith(b'%PDF'):
            raise ValueError('Response was not a PDF')
        (ROOT / filename).write_bytes(data)
        row.update(status='downloaded', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    except Exception as exc:
        row.update(status='failed', reason=str(exc))
    return row

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(fetch, SOURCES.items()))
    (ROOT / 'literature_downloads.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    print(json.dumps(rows, indent=2))
