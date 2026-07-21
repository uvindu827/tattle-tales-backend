from fastapi import FastAPI
from app.config import Settings
from app.routers import health
from app.routers import news

app = FastAPI(
    title=Settings.app_name,
    debug=Settings.debug,
)

app.include_router(health.router, prefix="/api/v1", tags=["Health Check"])
app.include_router(news.router, prefix="/api/v1", tags=["News"])

@app.get("/")
def root():
    return {
        "message": f"{Settings.app_name} is running",
        "docs": "/docs",
    }