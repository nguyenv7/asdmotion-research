# Data remain with the original owners

This repository contains research code and documentation, not a redistributed dataset. Raw data, processed tables, model weights and videos are excluded from Git. Local downloads are preserved on disk.

Owner: [Dinstein Lab — ASDMotion](https://github.com/Dinstein-Lab/ASDMotion). Consult the owner's README and terms for the current release.

| Owner-hosted artifact | Reference |
|---|---|
| Continuous skeleton archive, advertised without annotations | [asdpose.zip](https://drive.google.com/file/d/1MiNIhlf4mL-vRW1ub2TP3nCYzfMW0bYt/view) |
| Annotated skeleton clips | [dataset.pkl](https://drive.google.com/file/d/13t1tO4ZxTKmQG-w6fTy3hHQy8gX1bopl/view) |
| Released inference checkpoint | [model.pth](https://drive.google.com/file/d/1PuPXu6pfBYjz0G6NvWOEUQ_RvedvinAE/view) |
| Original paper | [Barami et al., JAMA Network Open, 2024](https://doi.org/10.1001/jamanetworkopen.2024.32851) |

## Raw video availability

Raw RGB video is **not included in the public ASDPose release**. The paper explains on page 9 that raw video is excluded to maintain privacy. The available motion files are skeletal representations; they cannot reconstruct the original video. Any possibility of separate controlled video access must be discussed with the data owners; no such access is established here.

## Reproduce locally

Run `python scripts/00_download.py` to download the three owner-hosted files into `data/raw/`, or follow the owner's links manually. About 13 GB is needed for the downloads. `data/raw/manifest.json` records the audited sizes and checksums, but contains no trajectories or model parameters.

Run the numbered analysis scripts to regenerate `data/processed/`. References to processed JSON/CSV files in research reports are local reproduction paths; those data files are intentionally absent from Git.
