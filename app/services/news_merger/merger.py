import logging

from .clustering import cluster_article
from .synthesis import synthesize_cluster
from .storage import save_merged_news
from .models import MergedNews
from app.services.news_scraper.storage import load_existing as load_raw_articles

logger = logging.getLogger(__name__)

def merge_all_articles() -> list[MergedNews]:
    raw_articles_dict = load_raw_articles()
    articles = list(raw_articles_dict.values())

    if not articles:
        logger.info("No raw articles found in the storage - nothing to merge")

        return []

    logger.info("Cluster %d raw articles...", len(articles))

    clusters = cluster_article(articles)

    logger.info("Formed %d clusters from %d articles", len(clusters), len(articles))

    merged_news = []
    for i, cluster in enumerate(clusters, start=1):
        logger.info(
            "Syntesizing cluster %d/%d (%d article(s))...",
            i, len(clusters), len(clusters)
        )

        story = synthesize_cluster(cluster)
        merged_news.append(story)

    return merged_news

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    stories = merge_all_articles()
    added = save_merged_news(stories)

    print(f"\nDone. Produced {len(stories)} merged stories this run, {added} were new.")