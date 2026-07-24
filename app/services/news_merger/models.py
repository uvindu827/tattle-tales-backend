from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib

@dataclass
class MergedNews:
    id: str
    headline: str
    merged_summary: str
    source_article_ids: list[str]
    source_names: list[str]
    category: str
    earliest_published: str
    latest_published: str
    merged_at: str

    @staticmethod
    def make_merged_news_id(article_ids: list[str]) -> str:
        """
        make an unique id for the merged news using single merged news ids
        """
        sorted_ids = sorted(article_ids)

        combined_id = ",".join(sorted_ids)

        return hashlib.sha256(combined_id.encode("utf-8")).hexdigest[:16]
    
@classmethod
def now_iso() -> str:
    """
    helper function to return current date time
    """

    return datetime.now(timezone.utc).isoformat()
