import requests
import logging

logger = logging.getLogger(__name__)

WIKIPEDIA_SEARCH_URL = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary"

REQUEST_TIMEOUT = 10  # seconds

def _find_best_matching_title(query:str, timeout:int) -> str | None:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": 1,
    }

    response = requests.get(WIKIPEDIA_SEARCH_URL, params=params, timeout=timeout)

    response.raise_for_status()
    data = response.json()

    results = data.get("query", {}).get("search", [])

    if not results:
        return None

    return results[0].get["title"]


def get_wikipedia_summary(query:str, timeout:int = REQUEST_TIMEOUT) -> dict | None:
    if not query or query.strip():
        return None

    try:
        title = _find_best_matching_title(query, timeout)

        if title is None:
            logger.info("No wikipedia articles found matching: %s", query)

            return None

        summary_url = f"{WIKIPEDIA_SUMMARY_URL}/{title.replace(' ', '_')}"

        response = requests.get(summary_url, timeout=timeout)

        if response.status_code == 404:
            logger.info("No wikipedia summary is found for title: %s", title)

            return None

        response.raise_for_status()

        data = response.json()

        return {
            "title": data.get("title", title),
            "extract": data.get("extract", ""),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
        }

    except requests.exceptions.RequestException as e:
        logger.warning("Wikipedia lookup failed for '%s' : '%s'", query, e)

        return None