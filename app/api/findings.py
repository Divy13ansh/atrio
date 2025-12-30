# app/api/findings.py
from fastapi import APIRouter, HTTPException
from app.db.memory import patients, images
from app.schemas.findings import (
    FindingsSummaryResponse,
    ImageFinding,
    FindingDetailResponse,
)

router = APIRouter(tags=["Findings"])

@router.get("/{patient_id}/findings-view", response_model=FindingsSummaryResponse)
def get_findings_summary(patient_id: str):
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")

    image_findings = []

    for image_id in patients[patient_id]["scans"]:
        img = images[image_id]
        findings = img["findings"]

        image_findings.append(
            ImageFinding(
                image_id=image_id,
                artery=findings["artery"] if findings else None,
                blockage_pct=findings["blockage_pct"] if findings else None,
                confidence=findings["confidence"] if findings else None,
            )
        )

    return FindingsSummaryResponse(
        patient_id=patient_id,
        images=image_findings
    )


@router.get(
    "/{patient_id}/findings-view/{image_id}",
    response_model=FindingDetailResponse
)
def get_finding_detail(patient_id: str, image_id: str):
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")

    if image_id not in images:
        raise HTTPException(status_code=404, detail="Image not found")

    image = images[image_id]

    if image["patient_id"] != patient_id:
        raise HTTPException(status_code=400, detail="Image does not belong to patient")

    if not image["findings"]:
        raise HTTPException(status_code=400, detail="Inference not run")

    return FindingDetailResponse(**image["findings"], image_id=image_id)
