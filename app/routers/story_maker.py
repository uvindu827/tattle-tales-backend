from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ..services.story_maker.story_maker import make_all_narrations
from ..services.story_maker.storage import save_narrations, load_existing
from ..schemas.narration_script import NarrationScriptOut, NarrationResults

router = APIRouter()

@router.post("/news/narrations", response_model=NarrationResults)
def trigger_Narration():
    scripts = make_all_narrations()
    added = save_narrations(scripts)

    return NarrationResults(
        total_processed=len(scripts),
        new_added=added,
        already_seen=len(scripts) - added,
    )

@router.get("/news/narration-scripts", response_model=list[NarrationScriptOut])
def list_narration_scripts(
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(50, ge=1, le=200, description="Max scripts to return")
):
    existing = load_existing()
    scripts = list(existing.values())

    if category:
        scripts = [s for s in scripts if s["category"] == category]

    scripts.sort(key=lambda s: s["created_at"], reverse=True)

    return scripts[:limit]

@router.get("/news/narration-scripts/{script_id}", response_model=NarrationScriptOut)
def get_narration_script(script_id: str):
    existing = load_existing()
    script = existing.get(script_id)

    if script is None:
        raise HTTPException(status_code=404, detail=f"Narration script '{script_id}' not found")

    return script

