from fastapi import FastAPI
from app.config import Settings
from app.routers import health

app = FastAPI(
    title=Settings.app_name,
    debug=Settings.debug,
)

app.include_router(health.router, prefix="/api/v1", tags=["Health Check"])

@app.get("/")
def root():
    return {
        "message": f"{Settings.app_name} is running",
        "docs": "/docs",
    }