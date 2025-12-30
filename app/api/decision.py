# app/api/decision.py
from fastapi import APIRouter, HTTPException
from app.db.memory import patients
from app.schemas.decision import AcceptRequest, RejectRequest
from app.services.decision_service import accept_findings, reject_findings

router = APIRouter(tags=["Decision"])

@router.post("/accept")
def accept(payload: AcceptRequest):
    if payload.patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")

    accept_findings(payload.patient_id)

    return {
        "patient_id": payload.patient_id,
        "status": "accepted"
    }


@router.post("/reject")
def reject(payload: RejectRequest):
    if payload.patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")

    reject_findings(payload.patient_id, payload.reason)

    return {
        "patient_id": payload.patient_id,
        "status": "rejected",
        "reason": payload.reason
    }
