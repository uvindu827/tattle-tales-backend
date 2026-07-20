import json
import os
import logging
from .models import NewsArticle

logger = logging.getLogger(__name__)

DEFAULT_STORE_PATH = os.path.join("data", "raw_articles.json")

def load_existing(path: str = DEFAULT_STORE_PATH) -> dict[str, dict]:
    """
    load existing articles 
    """
    if not os.path.exists(path):
        return {}
    
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)

            return {item["id"]: item for item in data}
        except json.JSONDecodeError:
            logger.warning("Existing store at %s is corrupted, starting fresh", path)

            return {}
        
def save_articles(new_articles: list[NewsArticle], path: str = DEFAULT_STORE_PATH ) -> int:
    """
    save new articles 
    """
    existing = load_existing(path)
    added = 0

    for article in new_articles:
        if article.id in existing:
            continue

        existing[article.id] = article.to_dict()
        added += 1

    parent_dir = os.path.dirname(path)

    if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
            json.dump(
                list(existing.values()), 
                f,
                indent = 2,
                ensure_ascii = False 
            )

            logger.info("Saved %d new articles, total articles: %d", added, len(existing))

            return added       

