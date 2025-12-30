# app/api/report.py
from fastapi import APIRouter, HTTPException
from app.db.memory import patients
from app.schemas.report import ReportResponse
from app.services.report_service import generate_report_for_patient

router = APIRouter(tags=["Report"])

@router.get("/report", response_model=ReportResponse)
def generate_report(patient_id: str):
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = patients[patient_id]

    if patient["decision_status"] != "accepted":
        raise HTTPException(
            status_code=400,
            detail="Report can only be generated after acceptance"
        )

    report = generate_report_for_patient(patient_id)
    return report
