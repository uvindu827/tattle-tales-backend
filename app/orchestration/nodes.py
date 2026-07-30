import logging

from .state import PipelineState

from ..services.news_scraper.scraper import scrape_all_sources
from ..services.news_scraper.storage import save_articles
from ..services.news_merger.merger import merge_all_articles
from ..services.news_merger.storage import save_merged_news
from ..services.story_maker.story_maker import make_all_narrations
from ..services.story_maker.storage import save_narrations

logger = logging.getLogger(__name__)

def scrape_node(state: PipelineState) -> dict:
    logger.info("[Pipeline] started from scraping stage")

    articles = scrape_all_sources()
    added = save_articles(articles)

    msg = f"Scraped {len(articles)} articles, {added} was new."

    logger.info("[Pipeline] %s", msg)

    return {
        "articles_scraped": len(articles),
        "new_articles": added,
        "log": [msg],
    }

def merge_node(state: PipelineState) -> dict:
    logger.info("[Pipeline] Started merge state")

    stories = merge_all_articles()
    added = save_merged_news(stories)

    msg = f"Merged {len(stories)} stories, {added} were new"

    logger.info("[Pipeline] %s", msg)

    return {
        "stories_merged": len(stories),
        "new_stories": added,
        "log": [msg],
    }

def narrate_node(state: PipelineState) -> dict:
    logger.info("[Pipeline] Started Narration stage")

    scripts = make_all_narrations()
    added = save_narrations(scripts)

    msg = f"Narrated {len(scripts)} scripts, {added} were new"

    logger.info("[Pipeline] %s", msg)

    return {
        "scripts_narrated": len(scripts),
        "new_scripts": added,
        "log": [msg],
    }