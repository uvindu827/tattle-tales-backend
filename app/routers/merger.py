from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ..services.news_merger.merger import merge_all_articles
from ..services.news_merger.storage import save_merged_news, load_existing
from ..schemas.merged_news import MergedNewsOut, MergeResult

router = APIRouter()

@router.post("/news/merge", response_model=MergeResult)
def trigger_merge():
    mergedNews = merge_all_articles()
    added = save_merged_news(mergedNews)

    return MergeResult(
        total_processed=len(mergedNews),
        new_added=added,
        already_seen=len(mergedNews) - added,
    )

@router.get("/news/merged-news", response_model=list[MergedNewsOut])
def list_merged_news(
    category: Optional[str] = Query(None, description="Filter by category"),
    source: Optional[str] = Query(None, description="Filter by source"),
    limit: int = Query(50, ge=1, le=200, description="Max number of stories to return")
):
    existing = load_existing()
    news = list(existing.values())

    if category:
        news = [
            n for n in news if s["category"] == category 
        ]

    if source:
        news = [
            n for n in news if s["source"] == source
        ]

    news.sort(key=lambda s: s["merged_at"], reverse=True)

    return news[:limit]

@router.get("/news/merged-news/{mergedNewsId}", response_model=MergedNewsOut)
def get_merged_news_by_Id(mergegedNewsId: str):
    existing = load_existing()
    news = existing.get(mergegedNewsId)

    if news is None:
        raise HTTPException(status_code=404, detail=f"Merged news {mergegedNewsId} not found!!")

    return news
