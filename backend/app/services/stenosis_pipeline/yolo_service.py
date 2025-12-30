from ultralytics import YOLO
import cv2
import numpy as np
import torch
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "ai_models" / "best.pt"

# ✅ Auto-select device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ✅ Load model once
yolo_model = YOLO(str(MODEL_PATH))
yolo_model.to(DEVICE)

def detect_stenosis(image_bytes):
    img = cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8),
        cv2.IMREAD_COLOR
    )

    # ✅ DO NOT pass device here
    results = yolo_model(img, conf=0.7)

    if len(results[0].boxes) == 0:
        return {"detected": False}

    box = results[0].boxes.xyxy[0].cpu().numpy()
    conf = float(results[0].boxes.conf[0])

    return {
        "detected": True,
        "box": box,
        "confidence": conf,
        "shape": img.shape
    }
