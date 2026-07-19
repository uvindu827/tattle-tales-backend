import feedparser
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def fetch_feed_entries(feed_url: str, max_entries: int = 5) -> list[dict]:
    """
    feed_url -> web address of the rss feed
    max_entries -> maximum number of entries fetching from the feed

    """

    parsed = feedparser.parse(feed_url)

    if parsed.bozo:
        logger.warning(
            "feed may be broken or unreachable: %s (reason: %s)",

            feed_url,
            parsed.get("bozo exception", "unknown error"),
        )

    entries = []

    for entry in parsed.entries[:max_entries]:
        entries.append({
            "title": entry.get("title", "").strip(),
            "link": entry.get("link", "").strip(),
            "published": _normalize_data(entry),
            "summary": entry.get("summary", "").strip(),
        })

    logger.info(
        "fetched %d entries from %s", len(entries), feed_url
    )

    return entries

def _normalize_data(entry) -> str:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6], tzinfo = timezone.utc)

        return dt.isoformat()
    
    return ""