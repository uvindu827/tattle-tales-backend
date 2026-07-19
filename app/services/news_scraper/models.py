from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib

@dataclass
class NewsArticle:
    id: str
    source: str
    title:str
    url: str
    published_at: str
    summary: str
    full_text: str
    category: str
    scraped_at: str

    @staticmethod
    def make_hashed_id(url: str) -> str:
        """Generates a unique id for news source url"""

        return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    
    def to_dict(self) -> dict:
        """Converts the NewsArticle dataclass to a dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data:dict) -> "NewsArticle":
        """Creates a news article object from the given dictionary"""
        return cls(**data)
    
def now_iso() -> str:
    """Returns the current UTC time in ISO 8601 format"""
    return datetime.now(timezone.utc).isoformat()
