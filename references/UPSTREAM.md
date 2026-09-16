# Original sources and local-only copies

The research repository references original owners. Downloaded papers, source copies, extracted source-page images, datasets and checkpoints are not committed.

- [ASDMotion owner repository](https://github.com/Dinstein-Lab/ASDMotion), audited commit `f699dc7b7af5726df5d8e79161d192eac22cfafb`.
- [ASDMotion's MMAction2 fork](https://github.com/TalBarami/mmaction2), audited commit `f632b7e56291805ac6d4debc8c7421b0d2c48f2e`.
- [Original JAMA paper](https://doi.org/10.1001/jamanetworkopen.2024.32851), with [PMC full text and supplements](https://pmc.ncbi.nlm.nih.gov/articles/PMC11393723/).
- [PoseC3D methods paper](https://openaccess.thecvf.com/content/CVPR2022/html/Duan_Revisiting_Skeleton-Based_Action_Recognition_CVPR_2022_paper.html).
- Additional papers: `literature_sources.json` and `references.bib` preserve author, date, DOI/URL and evidence status.

`python scripts/fetch_upstream.py` restores the pinned source files needed by the source-counterexample tests into ignored local directories. It never overwrites existing files. Paper download provenance is preserved in the small JSON manifests under `references/papers/`; PDF/text copies remain local. The source-code licenses belong to their respective owners.
