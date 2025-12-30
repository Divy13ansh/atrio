import os
import cv2
import uuid

from .yolo_service import detect_stenosis
from .roi_service import extract_roi
from .mask_service import segment_lumen
from .stenosis_service import compute_stenosis

RESULTS_DIR = "storage/results/visuals"

def run_stenosis_pipeline(image_bytes: bytes, image_name: str):
    yolo_out = detect_stenosis(image_bytes)

    if not yolo_out["detected"]:
        return None

    roi, meta = extract_roi(image_bytes, yolo_out, image_name)
    mask = segment_lumen(roi, image_name)
    result = compute_stenosis(roi, mask, meta)

    os.makedirs(RESULTS_DIR, exist_ok=True)

    visual_name = f"{uuid.uuid4()}_visual.png"
    visual_path = os.path.join(RESULTS_DIR, visual_name)
    cv2.imwrite(visual_path, result["visual"])

    return {
        "artery": result["artery"],
        "stenosis_percent": result["percent"],
        "severity": result["severity"],
        "confidence": yolo_out["confidence"],
        "visual_path": visual_path,
    }
