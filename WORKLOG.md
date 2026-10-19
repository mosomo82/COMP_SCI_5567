# Work Log

Shared record of who did what. Add one row per work session, with date, your name, what you did, and where the output is. Each member edits only their own rows. This supports fair credit and the individual questionnaire.

**Note:** rows for Rehan Ali and Bosia N'dri were filled by Tony from the Pipeline A repository, the meeting document, and the team deck draft. Please check your rows, correct the dates and details, and add anything missing.

Team: Tony Nguyen, Rehan Ali, Bosia N'dri. Pipeline A (Faster R-CNN + Siamese ReID + own tracker): Rehan and Bosia. Pipeline B (YOLO + ReID + BoT-SORT + repair) and the comparison: Tony.

## Team meetings and decisions

Source: team meeting document (colour code: Tony blue, Rehan red, Bosia green, Team yellow).

| Date | Who | What was decided or assigned |
|---|---|---|
| 2026-09-23 | Team | Kickoff. Midterm is mid-October, 15 minutes: workload, timeline, current progress, methods. Everyone researches the proposed topics. Topic to be finalized on Sep 24 after 8:00 PM. |
| 2026-09-23 | Rehan | Contact the professor to clarify the midterm presentation expectations. |
| 2026-09-26 | Team | Second meeting. Shortlist: toll booth tracking or human video tracking. Everyone researches datasets; the topic with the strongest available data wins. Next meeting Sep 29, 3:30 PM. |
| After 2026-09-26 | Team | Professor fixed the topic: human video tracking (offline MOT) with the provided training data only. Preparation tasks for everyone: parse the ground-truth files, torchvision augmentation, fine-tune a pre-trained Faster R-CNN on Colab (T4 GPU), study Siamese networks for ReID (the note says "build from scratch"; open question for the instructor, see below). |
| 2026-10-15| Team | Meeting to go through each person's pipeline and the presentation. No minutes were written in the meeting document. |
| 2026-10-22 | Team | Midterm presentation. Speakers: Bosia slides 1, 2, 11, 12; Rehan slides 3, 4, 5, 10; Tony slides 6, 7, 8, 9. |

Open question: the meeting document says the Siamese network must be built from scratch. Both pipelines start from ImageNet weights. Check the course video or ask the instructor.

## Contribution log

| Date | Member | Work done | Output / location |
|---|---|---|---|
| 2026-10-15 | Tony Nguyen | Downloaded MOT16 to Drive, validated ground-truth boxes on a frame | `results/gt_check.png`, notebook 01 |
| 2026-10-15 | Tony Nguyen | Converted MOT16 to YOLO format (split by sequence, val = MOT16-09) | notebook 02, `yolo_mot16.zip` on Drive |
| 2026-10-15 | Tony Nguyen | Fine-tuned YOLO26m at 960 px; compared with pretrained (mAP50 0.792 to 0.872 on MOT16-09) | notebook 03, `results/detector_pretrained_vs_finetuned.csv`, `results/detector_training_curves.png`, `results/results.csv` |
| 2026-10-15 | Tony Nguyen | Added `.gitignore`, `README.md`, `WORKLOG.md` | repo root |
| 2026-10-15 | Tony Nguyen | Ran augmentation experiment (scale 0.5 vs 0.0, 10 epochs each) | `results/augmentation_experiment.csv` |
| 2026-10-15 | Tony Nguyen | Side-by-side pretrained vs fine-tuned detections on a MOT16-09 frame | `results/qualitative_pretrained_vs_finetuned.png` |
| 2026-10-15 | Tony Nguyen | Saved training config (30 epochs, 960 px, batch 8, seed 42, A100) | `results/detector_training_config.json` |
| 2026-10-16 | Tony Nguyen | Tracking with ByteTrack and BoT-SORT scored by TrackEval (E0 to E2), threshold sweeps, false-negative analysis | notebook 04, Drive `results/` |
| 2026-10-16 | Tony Nguyen | ReID model (ResNet-50 + BNNeck, ID + triplet loss) and the split/merge repair step | notebook 05 |
| 2026-10-16 | Tony Nguyen | Test-sequence inference: target videos on MOT16-03 and MOT16-14, notes on failures | notebook 06, `results/notes_MOT16-03.md` |
| 2026-10-16 | Rehan Ali | Pipeline A repository: Faster R-CNN fine-tuning, Siamese ReID (ResNet-18, triplet loss), own tracker (Kalman, Hungarian, gating, offline rules), own metric code, notebooks 01 to 05, tables, figures, LaTeX report draft, MOT16-01 target video | [Pipeline A repository](https://github.com/Rehan-rahim/mot16-pedestrian-tracking_project) |
| 2026-10-16 | Bosia N'dri | Pipeline A models with Rehan: Faster R-CNN fine-tuning and Siamese ReID training (per the team deck draft) | Pipeline A repository, notebooks 02 and 03 `[Bosia to confirm and add details]` |
| 2026-10-16 | Rehan Ali, Bosia N'dri | Midterm deck draft (15 slides, Pipeline A story) with speaker notes | team deck file |
| 2026-10-16 | Rehan Ali | Shared Pipeline A weights and cached detections for the comparison `[Rehan to confirm date]` | Drive folder `DL_Project_MOT` |
| 2026-10-17 | Tony Nguyen | Pipeline comparison with one evaluator: saved tracks (TrackEval), detectors, detector swap, ReID protocol, per-person analysis, speed | `notebooks/07_pipeline_comparison.ipynb`, Drive `results/` |
| 2026-10-17 | Tony Nguyen | Comparison and review documents: pipeline comparison, review of the Pipeline A report, numbers audit | `docs/PIPELINE_COMPARISON.md`, `docs/REPORT_REVIEW.md`, `docs/REPORT_NUMBERS_AUDIT.md` |
| 2026-10-17 | Tony Nguyen | Combined LaTeX report (11 to 12 pages) with tables, figures, and bibliography | `report/main.tex`, `report/refs.bib`, `report/Combined_Report.pdf` |
| 2026-10-17 | Tony Nguyen | Report writing prompt (mega prompt) and midterm outline with speaker notes | `docs/MEGA_PROMPT.md`, `docs/MIDTERM_DECK_REVIEW_AND_OUTLINE.md` |
| 2026-10-17 | Tony Nguyen | Combined midterm deck (first version): 12 slides plus 3 backup slides, embedded target videos | `report/MOT16_Midterm_Combined_Deck_v2.pptx` |
| 2026-10-18 | Tony Nguyen | Remade the midterm deck around the four required parts (workload, timeline, current progress, methodology): 15 slides (14 minutes) plus 3 backup slides, speaker notes, embedded target videos | `report/MOT16_Midterm_Deck_v3.pptx` |

## Experiments (parameters changed and effect)

All on MOT16-09 (held out). Single runs unless stated; settings were chosen on this same sequence.

| Date | Member | Parameter changed | Result |
|---|---|---|---|
| 2026-10-15 | Tony Nguyen | YOLO `scale` augmentation 0.5 to 0.0 (10 epochs, seed 42) | Precision 0.901 to 0.948, recall 0.748 to 0.736, mAP50 0.867 to 0.864, mAP50-95 0.587 to 0.580. Single seed; the mAP change is within noise. |
| 2026-10-16 | Tony Nguyen | Detector and tracker: pretrained YOLO + ByteTrack (E0), fine-tuned YOLO + ByteTrack (E1), fine-tuned YOLO + BoT-SORT (E2) | HOTA 48.11, 47.94, 48.40; IDF1 57.37, 55.77, 55.65; ID switches 46, 42, 46; MOTA 59.29, 64.77, 68.54 |
| 2026-10-16 | Tony Nguyen | ReID repair thresholds (split none, 0.5, 0.4; merge 0.25, 0.35, 0.45) on E2 | Best split 0.5, merge 0.35: HOTA 48.40 to 55.30, IDF1 55.65 to 68.04, but ID switches 46 to 56. Merge only (0.35): IDF1 62.58, 42 switches. Split 0.4 cuts too often (74 to 75 switches). |
| 2026-10-17 | Tony Nguyen | YOLO detections inside Pipeline A's tracker; score thresholds 0.7/0.6, 0.6/0.5, 0.5/0.4, 0.4/0.3 | Misses 1,609 to 1,208 and AssA 44.57 to 38.40 as thresholds fall; fewest ID switches (21) at 0.7/0.6; best HOTA 51.08 at 0.6/0.5 |
| 2026-10-16 | Rehan Ali, Bosia N'dri | Pipeline A tracker ablation (steps added one by one) | IDF1 47.7 (IoU only), 56.2 (+ Kalman), 62.2 (+ Siamese), 60.2 (+ low-score pass), 60.3 (+ exit rule and gap fill); ID switches 71, 43, 34, 38, 35. Source: Pipeline A `ablation.csv`. |

## Next steps

| Task | Owner | Status |
|---|---|---|
| Confirm roles, dates, and the worklog rows of Rehan and Bosia | Rehan, Bosia | open |
| Midterm presentation (Oct 22) and rehearsals | all | open |
| Second validation sequence | all | open |
| Final report: finish figures, check bibliography entries, proofread | all | in progress (`report/main.tex`) |
| Final presentation and target video on a MOT16 test sequence | all | open (date to be announced) |
| Individual anonymous questionnaire | each member | open |
| Answer the "Siamese from scratch" question with the instructor | Rehan | open |
