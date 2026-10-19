# Offline Multi-Pedestrian Tracking on MOT16: Two Pipelines Compared

**CS 5567 Deep Learning · University of Missouri–Kansas City**
Team: Tony Nguyen · Rehan Ali · Bosia N'dri

Multi-object tracking follows every pedestrian in a video and keeps one ID per person, even through occlusion. We built **two** offline tracking-by-detection pipelines for the MOT16 benchmark and compare them with the same evaluation code on a held-out sequence.

| | Pipeline A (course template) | Pipeline B (modernized) |
|---|---|---|
| Built by | Rehan Ali, Bosia N'dri | Tony Nguyen |
| Detector | Faster R-CNN (torchvision, backbone frozen) | YOLO (`yolo26m`, all layers fine-tuned) |
| ReID | Siamese ResNet-18, 128-d, triplet loss | ResNet-50 + BNNeck, 2048-d, ID loss + triplet loss |
| Tracker | Own tracker: Kalman filter, Hungarian matching, gating, two passes, offline rules | BoT-SORT (library) + our appearance-based split/merge repair |
| Metric code | Own code, checked against TrackEval | TrackEval |
| Code | [Pipeline A repository](https://github.com/Rehan-rahim/mot16-pedestrian-tracking_project) | `notebooks/` in this repository |

> **Status (midterm, Oct 22, 2026):** both pipelines are complete and compared on MOT16-09. Remaining: a second validation sequence, the final report, and the final presentation. Every number below was computed by the team; sources are named.

## Pipelines

```
Pipeline A:  frame -> Faster R-CNN -> boxes -> Siamese ReID -> embeddings -> own tracker -> boxes + IDs
Pipeline B:  frame -> YOLO -> boxes -> BoT-SORT -> tracks -> ReID embeddings -> split/merge repair -> boxes + IDs
```

## Results (held-out sequence MOT16-09)

Train on MOT16-02, 04, 05, 10, 11, 13; validate on MOT16-09 (525 frames, 25 identities, 5,257 evaluated boxes). Both pipelines use this split. All scores below were tuned on MOT16-09 and are therefore optimistic.

**Tracking (TrackEval, Notebook 07)**

| Run | HOTA | DetA | AssA | MOTA | IDF1 | ID switches |
|---|---|---|---|---|---|---|
| A: published tracks | 50.40 | 53.97 | 47.11 | 55.83 | 60.35 | 35 |
| B: YOLO + BoT-SORT | 48.40 | 60.36 | 38.95 | 68.54 | 55.65 | 46 |
| B: BoT-SORT + repair | 55.30 | 60.25 | 50.89 | 68.35 | 68.04 | 56 |
| Hybrid: YOLO detections in A's tracker (0.6 / 0.5) | 51.08 | 58.18 | 44.93 | 67.38 | 62.65 | 30 |

**Detection (same evaluator, all 525 frames):** AP@0.5 0.7896 (B) and 0.7798 (A). At precision 0.80, recall on heavily hidden people (visibility below 0.25) is 0.471 (B) against 0.316 (A); overall 0.798 against 0.757.

**ReID (common protocol):** A trained: mAP 0.635, Rank-1 0.767. B trained: mAP 0.844, Rank-1 0.922. The two models differ in size and input, and B's checkpoint was chosen on MOT16-09.

**Per person (18 people with at least 100 frames):** at most 2 are tracked perfectly (one ID covering at least 90% of their frames) by any run.

**Target videos:** Pipeline A, MOT16-01, ID 11, frames 1 to 361. Pipeline B, MOT16-14, ID 215, highlighted in about frames 544 to 724. Videos and result files: [Drive results folder](https://drive.google.com/drive/folders/19Z_0Swv9Cj_GKvjMxshVTRSGltaQ7dk9).

**Pipeline B detector (own evaluation, [`results/detector_pretrained_vs_finetuned.csv`](results/detector_pretrained_vs_finetuned.csv)):**

| Model | Precision | Recall | mAP@50 | mAP@50-95 |
|---|---|---|---|---|
| YOLO26m pretrained (COCO) | 0.904 | 0.728 | 0.792 | 0.511 |
| YOLO26m fine-tuned on MOT16 | 0.905 | 0.780 | 0.872 | 0.591 |

Training: 30 epochs, 960 px, batch 8, seed 42, cosine LR, NVIDIA A100-SXM4-40GB (about 91 min); setup in [`results/detector_training_config.json`](results/detector_training_config.json), curves in [`results/detector_training_curves.png`](results/detector_training_curves.png).

**Experiments with the code (details in `WORKLOG.md`):** augmentation `scale` 0.5 vs 0.0 ([`results/augmentation_experiment.csv`](results/augmentation_experiment.csv)); repair thresholds (split and merge); score thresholds of the hybrid; ablation of Pipeline A's tracker.

**Main limits:** one validation sequence; thresholds and checkpoints chosen on it; YOLO and Faster R-CNN scores are on different scales; speeds were measured on different GPUs; target videos are clean examples and test sequences have no public labels.

## Repository layout

```
notebooks/   Colab notebooks of Pipeline B and the comparison, run in order 01 -> 07
report/      LaTeX report (US letter, 11 pt), figures, bibliography, compiled PDF, midterm deck (v3)
docs/        analysis and planning documents, course PDFs
results/     tables, figures, logs, notes
src/         run_tracking.py (starter script)
configs/     reserved for settings files (empty for now)
data/        MOT16 (gitignored, see Setup)
```

| Notebook | Purpose | Owner |
|---|---|---|
| `01_data_setup_and_validation` | Download MOT16, check the ground truth, first detector check | Tony |
| `02_yolo_dataset_preparation` | Convert MOT16 to YOLO format (split by sequence) | Tony |
| `03_detector_finetuning` | Fine-tune YOLO26, compare with pretrained, augmentation experiment | Tony |
| `04_tracking_and_evaluation` | BoT-SORT and ByteTrack, TrackEval, sweeps, false-negative analysis | Tony |
| `05_reid_appearance_model` | ReID model (ID + triplet loss) and the split/merge repair | Tony |
| `06_test_sequence_inference` | Single-target videos on MOT16 test sequences | Tony |
| `07_pipeline_comparison` | Pipeline A vs B with one evaluator: tracks, detectors, detector swap, ReID, per-person, speed | Tony (uses Pipeline A files from Rehan and Bosia) |

Pipeline A's notebooks (01–05), source code and report draft are in the [Pipeline A repository](https://github.com/Rehan-rahim/mot16-pedestrian-tracking_project) (Rehan, Bosia).

Key documents in `docs/`: [`PIPELINE_COMPARISON.md`](docs/PIPELINE_COMPARISON.md), [`REPORT_REVIEW.md`](docs/REPORT_REVIEW.md), [`REPORT_NUMBERS_AUDIT.md`](docs/REPORT_NUMBERS_AUDIT.md), [`MIDTERM_DECK_REVIEW_AND_OUTLINE.md`](docs/MIDTERM_DECK_REVIEW_AND_OUTLINE.md), [`MEGA_PROMPT.md`](docs/MEGA_PROMPT.md), `IMPLEMENTATION_PLAN.md`.

## Setup

Code runs on **Google Colab** (GPU runtime); HellBender (Mizzou HPC) is optional for long benchmark jobs.

1. Open a notebook in Colab and choose a GPU runtime.
2. Notebook 01 mounts Drive and downloads MOT16 once into `MyDrive/MOT16_project/`. MOT16 ([motchallenge.net/data/MOT16](https://motchallenge.net/data/MOT16/), about 1.9 GB) is not committed.
3. Run notebooks 01 to 06 in order. Notebook 07 also needs three files of Pipeline A in `MyDrive/MOT16_project/Backup/pipelineA/`: `detector_frcnn_mot16.pth`, `reid_resnet18_triplet.pth`, `MOT16-09_finetuned.pkl` (from Rehan; weights are not in either repository).

## Evaluation protocol

- Metrics: HOTA, DetA, AssA, MOTA, IDF1, ID switches, false positives and misses via TrackEval on MOT16 train sequences (test labels are not public).
- Split by sequence, never by frame; the detector and ReID models are not evaluated on sequences they trained on.
- One detector evaluator for both detectors (IoU 0.5, one-to-one matching, "don't care" regions ignored) and one ReID query/gallery protocol for all models.
- Speed is reported with the GPU model.

## Model weights

Weights are not stored in this repository (course rule and size). Pipeline B's `yolo_mot16_best.pt` and `reid_best.pt` are on the team Google Drive: *add link here*.

## Team and roles

| Member | Role |
|---|---|
| Rehan Ali | Pipeline A (design and integration, own tracker, metric code, MOT16-01 target video, report draft); contact with the professor |
| Bosia N'dri | Pipeline A (models: Faster R-CNN fine-tuning, Siamese ReID training, per the team deck draft); midterm demo and closing |
| Tony Nguyen | Pipeline B (YOLO, ReID, repair), TrackEval evaluation and the comparison of both pipelines, combined report and deck |

Roles of Rehan and Bosia were written from the Pipeline A repository and the team deck; please correct them. Dated contributions are in `WORKLOG.md`.

## Timeline

| Date | Milestone |
|---|---|
| Sep 23, 2026 | Kickoff: midterm requirements (15 minutes) |
| Sep 26, 2026 | Topic shortlist and dataset search |
| After Sep 26 | Topic fixed by the professor: human video tracking (offline MOT) on the provided data |
| Oct 15–17 | Pipeline B, Pipeline A repository, comparison notebook, report draft, combined deck |
| Oct 22, 2026 | Midterm presentation |
| Final (date to be announced) | Final presentation, source code, target video on a MOT16 test sequence, PDF report (at least 4 pages), individual anonymous questionnaire |

## References

- Ren et al., *Faster R-CNN*, NeurIPS 2015. Redmon et al., *YOLO*, CVPR 2016. Ultralytics YOLO: https://docs.ultralytics.com
- Hermans et al., *In Defense of the Triplet Loss*, 2017. Luo et al., *Bag of Tricks for Person Re-ID*, CVPRW 2019.
- Bewley et al., *SORT*, 2016. Wojke et al., *DeepSORT*, 2017. Zhang et al., *ByteTrack*, ECCV 2022. Aharon et al., *BoT-SORT*, 2022.
- Milan et al., *MOT16*, 2016. Luiten et al., *HOTA*, IJCV 2021. TrackEval: https://github.com/JonathonLuiten/TrackEval
- Full list: [`report/refs.bib`](report/refs.bib).
