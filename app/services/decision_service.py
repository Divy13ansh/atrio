from app.db.memory import patients

def accept_findings(patient_id: str):
    patients[patient_id]["decision_status"] = "accepted"
    patients[patient_id]["decision_feedback"] = None
    patients[patient_id]["report_generated"] = False


def reject_findings(patient_id: str, reason: str):
    patients[patient_id]["decision_status"] = "rejected"
    patients[patient_id]["decision_feedback"] = reason
    patients[patient_id]["inference_status"] = "needs_review"
