import logging
import time

from .sources import MAX_ARTICLES_PER_SOURCE, NEWS_SOURCES
from .fetch_rss import fetch_feed_entries
from .extract_content import extract_full_text
from .models import NewsArticle, now_iso
from .storage import save_articles

logger = logging.getLogger(__name__)

def scrape_all_sources() -> list[NewsArticle]:
    """
    Scrape all news sources and return a list of new articles.
    """
    allArticles: list[NewsArticle] = []

    for source in NEWS_SOURCES:
        logger.info("Scraping source: %s", source["name"])

        entries = fetch_feed_entries(source["url"], max_entries=MAX_ARTICLES_PER_SOURCE)

        for entry in entries:

            if not entry["link"]:
                logger.info("Skipping an entry with no link from %s", source["name"])
                continue

            full_text = extract_full_text(entry["link"])

            article = NewsArticle(
                id = NewsArticle.make_hashed_id(entry["link"]),
                source = source["name"],
                title = entry["title"],
                url = entry["link"],
                published_at = entry["published"],
                summary = entry["summary"],
                full_text = full_text,
                category = source["category"],
                scraped_at = now_iso()
            )

            allArticles.append(article)

            # wait for half a second to avoid hitting the server continuosly
            time.sleep(0.5) 

    return allArticles

if __name__  == "__main__":
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(name)s : %(message)s",
    )

    articles = scrape_all_sources()
    added = save_articles(articles)

    print(f"\nDone. Scraped {len(articles)} articles this run \n {added} articles were new")
