import json
import os
import logging

from .models import MergedNews

logger = logging.getLogger(__name__)

DEFAULT_STORE_PATH = os.path.join("data", "merged_news.json")

def load_existing(path: str = DEFAULT_STORE_PATH) -> dict[str, dict]:
    
    if not os.path.exists(path):
        return {}
    
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)

            return {
                item["id"]: item for item in data
            }

        except json.JSONDecoderError:
            logger.warning("Existing store at %s corrupted. Starting fresh", path)

            return {}
        
def save_merged_news(new_news: list[MergedNews], path: str = DEFAULT_STORE_PATH) -> int:

    existing = load_existing(path)
    added = 0

    for news in new_news:
        #debugging lines for to_dict error
        print(type(news))
        print(news)
        print(isinstance(news, MergedNews))

        if news.id in existing:
            continue

        existing[news.id] = news.to_dict()
        added += 1

    parent_dir = os.path.dirname(path)

    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            list(existing.values()),
            f,
            indent=2,
            ensure_ascii=False
        )

    logger.info("Saved %d new merged news, total stories %d", added, len(existing))

    return added