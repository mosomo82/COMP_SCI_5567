# Work Log

Shared record of who did what. Add one row per work session, with date, your name, what you did, and where the output is. Each member edits only their own rows. This supports fair credit and the individual questionnaire.

| Date | Member | Work done | Output / location |
|---|---|---|---|
| 2026-10-15 | Tony Nguyen | Downloaded MOT16 to Drive, validated ground-truth boxes on a frame | `results/gt_check.png`, notebook 01 |
| 2026-10-15 | Tony Nguyen | Converted MOT16 to YOLO format (split by sequence, val = MOT16-09) | notebook 02, `yolo_mot16.zip` on Drive |
| 2026-10-15 | Tony Nguyen | Fine-tuned YOLO26m at 960 px; compared with pretrained (mAP50 0.792 -> 0.872 on MOT16-09) | notebook 03, `results/detector_pretrained_vs_finetuned.csv`, `results/detector_training_curves.png`, `results/results.csv` |
| 2026-10-15 | Tony Nguyen | Added `.gitignore`, `README.md`, `WORKLOG.md` | repo root |
| 2026-10-15 | Tony Nguyen | Ran augmentation experiment (scale 0.5 vs 0.0, 10 epochs each) | `results/augmentation_experiment.csv` |
| 2026-10-15 | Tony Nguyen | Side-by-side pretrained vs fine-tuned detections on a MOT16-09 frame | `results/qualitative_pretrained_vs_finetuned.png` |
| 2026-10-15 | Tony Nguyen | Saved training config (30 epochs, 960 px, batch 8, seed 42, A100) | `results/detector_training_config.json` |
| | Rehan Ali | | |
| | Bosia N'dri | | |

## Experiments (parameters changed and effect)

| Date | Member | Parameter changed | Result |
|---|---|---|---|
| 2026-10-15 | Tony Nguyen | `scale` augmentation 0.5 -> 0.0 (10 epochs, seed 42, val MOT16-09) | Precision 0.901 -> 0.948, recall 0.748 -> 0.736, mAP50 0.867 -> 0.864, mAP50-95 0.587 -> 0.580. Single seed; mAP change is within noise. |
