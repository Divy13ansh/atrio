# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.router import router
from app.core.config import settings

app = FastAPI(
    title="Angio AI Platform",
    description="AI-assisted angiography analysis & reporting",
    version="0.1.0"
)

# Register routes
app.include_router(router)

app.mount("/storage", StaticFiles(directory="storage"), name="storage")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "angio-ai",
        "env": settings.ENV
    }
