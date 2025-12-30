from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.dashboard import DashboardResponse, DashboardPatient
from app.services.dashboard_service import fetch_dashboard

router = APIRouter(tags=["Dashboard"])

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    rows = await fetch_dashboard(db)

    patients = [
        DashboardPatient(
            patient_id=str(row.patient_id),
            name=row.name,
            scans=row.scans,
            inference_status="not_started",   # placeholder (next step)
            decision_status="pending",        # placeholder (next step)
            report_generated=False,           # placeholder (next step)
        )
        for row in rows
    ]

    return DashboardResponse(patients=patients)
