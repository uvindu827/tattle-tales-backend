from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ..services.news_scraper.scraper import scrape_all_sources
from ..services.news_scraper.storage import save_articles, load_existing
from ..schemas.article import ArticleOut, ScrapeResult

router = APIRouter()

@router.post(path="/news/scrape", response_model=ScrapeResult)
def trigger_scrape():
    """
    API for scrape all resources and save articles to storage
    """
    articles = scrape_all_sources()

    added = save_articles()

    return ScrapeResult(
        total_processed=len(articles),
        new_added=added,
        already_seen=len(articles) - added,
    )

@router.get(path="/news/articles", response_model=list[ArticleOut])
def list_articles(
    source: Optional[str] = Query(None, description="Filter by exact source name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(50, ge=1, le=200, description="Max number if articles to return"),
):
    """
    get all articles in the store
    """
    existing = load_existing()

    articles = list(existing.values())

    if source:
        articles = [
            article for article in articles if article["source"] == source
        ]

    if category:
        articles = [
            article for article in articles if article["category"] == category
        ]

    articles.sort(key=lambda article: article["scraped_at"], reverse=True)

    return articles[:limit]

@router.get(path="/news/articles/{article_id}",  response_model=ArticleOut)
def get_article(article_id:str):
    """
    get a single article by its id
    """
    existing = load_existing()
    article = existing.get(article_id)

    if article is None:
        raise HTTPException(
            status_code=404,
            detail=f"Article '{article_id}' not found"
        )
    
    return article



