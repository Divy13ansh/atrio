# app/api/inference.py
from fastapi import APIRouter, HTTPException
from app.db.memory import patients
from app.services.inference_service import run_inference_for_patient

router = APIRouter(tags=["Inference"])

@router.post("/{patient_id}/run-inference")
def run_inference(patient_id: str):
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")

    if not patients[patient_id]["scans"]:
        raise HTTPException(status_code=400, detail="No scans uploaded")

    run_inference_for_patient(patient_id)

    return {
        "patient_id": patient_id,
        "status": "inference completed",
        "images_processed": len(patients[patient_id]["scans"])
    }
