# 0002 — Public repository with owner-hosted data

Date: 2026-09-16. Status: accepted by user.

Publish the research companion at https://github.com/nguyenv7/asdmotion-research as a public repository. Include authored analysis code, research documentation, LaTeX source, the compiled dossier, small explanatory figures, and source/download manifests. Reference Dinstein Lab and the original paper prominently.

Keep all downloaded datasets, derived record-level tables, model weights, source snapshots, source-paper PDFs, environments, logs and temporary tools local and Git-ignored. Retain owner URLs and hashes for reproducibility. Do not delete local research inputs. Run `scripts/check_git_payload.py` after staging; every tracked file must be below 1 MB.

The paper explicitly excludes raw videos from public sharing for privacy (Barami et al., 2024, p. 9, Data Sharing Statement). Skeleton trajectories are the available public modality; RGB-dependent work requires a separate lawful source/access arrangement. The repository does not grant new rights over owner-hosted data or third-party publications.

The portable analysis package versions are recorded in `requirements-analysis-lock.txt`; the full machine-specific environment freeze stays local. Pinned owner code needed by audit tests can be fetched with `scripts/fetch_upstream.py`.
