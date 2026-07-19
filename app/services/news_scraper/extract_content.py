import trafilatura
from trafilatura.settings import use_config
import logging

logger = logging.getLogger(__name__)

def _build_config(timeout: int):
    """
    override the default time out confoguration of trfilature
    """
    config = use_config()
    config.set("DEFAULT", "DOWNLOAD_TIMEOUT", str(timeout))

    return config

def extract_full_text(url: str, timeout: int = 10) -> str:
    """
    downloads the full article from news site and extract the article part only
    """
    try:
        #Download article
        config = _build_config(timeout)
        downloaded = trafilatura.fetch_url(url, config=config)

        if downloaded is None:
            logger.warning("Couldn't download article - url: %s", url)
            return ""
        
        #extract content
        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            favor_precision=True,
        )

        return text or ""
    
    except Exception as e:
        logger.error("Extraction failed for url: %s with error: %s", url, e)

        return ""
