from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def fetch_dashboard(db: AsyncSession):
    query = text("""
        SELECT
            p.id              AS patient_id,
            p.name            AS name,
            COUNT(i.id)       AS scans
        FROM patients p
        LEFT JOIN studies s ON s.patient_id = p.id
        LEFT JOIN images i  ON i.study_id = s.id
        GROUP BY p.id, p.name
        ORDER BY p.created_at DESC
    """)

    result = await db.execute(query)
    return result.fetchall()
