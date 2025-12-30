# app/services/report_service.py
from app.db.memory import patients, images

def generate_report_for_patient(patient_id: str):
    patient = patients[patient_id]

    findings = []

    for image_id in patient["scans"]:
        img = images[image_id]
        f = img["findings"]

        findings.append({
            "image_id": image_id,
            "artery": f["artery"],
            "blockage_pct": f["blockage_pct"],
            "confidence": f["confidence"],
        })

    # deterministic summary (important)
    max_blockage = max(f["blockage_pct"] for f in findings)
    summary = f"Maximum detected stenosis: {max_blockage}%."

    patient["report_generated"] = True

    return {
        "patient_id": patient_id,
        "summary": summary,
        "findings": findings,
        "generated": True,
    }
