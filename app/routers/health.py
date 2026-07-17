from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "Status": "OK",
        "time": datetime.now(timezone.utc).isoformat(),
    }
