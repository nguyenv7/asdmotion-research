"""Extract source pages and searchable text; never reconstruct published figures."""
from pathlib import Path
import json
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images-from-papers"
OUT.mkdir(exist_ok=True)
manifest = []
for stem, pages in {
    "Barami2024_JAMA": [4, 7, 8],
    "Barami2024_supplement1": [4, 6, 7, 8],
}.items():
    document = pymupdf.open(ROOT / "references" / "papers" / f"{stem}.pdf")
    (ROOT / "references" / "papers" / f"{stem}.txt").write_text(
        "\n".join(f"PAGE {i + 1}\n{page.get_text()}" for i, page in enumerate(document)),
        encoding="utf-8",
    )
    for page_number in pages:
        target = OUT / f"{stem}-page{page_number}.png"
        document[page_number - 1].get_pixmap(dpi=120).save(target)
        manifest.append({"source": f"references/papers/{stem}.pdf", "page": page_number,
                         "output": target.relative_to(ROOT).as_posix(), "method": "unmodified full-page rendering"})
(OUT / "paper_assets_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"Rendered {len(manifest)} original source pages.")
