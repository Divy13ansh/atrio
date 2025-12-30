# app/services/inference_service.py
from app.db.memory import patients, images, generate_mock_findings

def run_inference_for_patient(patient_id: str):
    patient = patients[patient_id]

    patient["inference_status"] = "running"

    for image_id in patient["scans"]:
        images[image_id]["findings"] = generate_mock_findings()

    patient["inference_status"] = "completed"
