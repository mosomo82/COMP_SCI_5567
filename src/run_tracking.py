"""Starter: detect + track pedestrians on a MOT16 sequence and export MOT-format results.

Usage:
    python starter/run_tracking.py --seq data/MOT16/train/MOT16-09 --tracker bytetrack.yaml
    python starter/run_tracking.py --seq data/MOT16/train/MOT16-09 --tracker botsort.yaml

Output: results/<seq>_<tracker>.txt  (frame,id,x,y,w,h,conf,-1,-1,-1) for TrackEval
        results/<seq>_<tracker>.mp4  (annotated video)
NOTE: untested scaffold - verify against your installed ultralytics version.
"""
import argparse
from pathlib import Path

import cv2
from ultralytics import YOLO


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", required=True, help="MOT16 sequence dir containing img1/")
    ap.add_argument("--weights", default="yolo26m.pt", help="pretrained or fine-tuned weights")
    ap.add_argument("--tracker", default="bytetrack.yaml")
    ap.add_argument("--conf", type=float, default=0.25)
    ap.add_argument("--imgsz", type=int, default=960)
    args = ap.parse_args()

    seq = Path(args.seq)
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)
    stem = f"{seq.name}_{Path(args.tracker).stem}"

    model = YOLO(args.weights)
    frames = sorted((seq / "img1").glob("*.jpg"))
    h, w = cv2.imread(str(frames[0])).shape[:2]
    video = cv2.VideoWriter(str(out_dir / f"{stem}.mp4"),
                            cv2.VideoWriter_fourcc(*"mp4v"), 30, (w, h))

    lines = []
    for i, f in enumerate(frames, start=1):
        # classes=[0] -> COCO "person"; persist=True keeps tracker state across calls
        r = model.track(str(f), persist=True, tracker=args.tracker,
                        classes=[0], conf=args.conf, imgsz=args.imgsz, verbose=False)[0]
        if r.boxes.id is not None:
            for (x1, y1, x2, y2), tid, c in zip(r.boxes.xyxy.tolist(),
                                                r.boxes.id.int().tolist(),
                                                r.boxes.conf.tolist()):
                lines.append(f"{i},{tid},{x1:.2f},{y1:.2f},{x2 - x1:.2f},{y2 - y1:.2f},{c:.4f},-1,-1,-1")
        video.write(r.plot())  # draws boxes + IDs

    video.release()
    (out_dir / f"{stem}.txt").write_text("\n".join(lines) + "\n")
    print(f"Wrote {len(lines)} track rows over {len(frames)} frames -> results/{stem}.*")


if __name__ == "__main__":
    main()
