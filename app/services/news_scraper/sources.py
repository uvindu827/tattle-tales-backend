NEWS_SOURCES = [
    {
        "name": "BBC news",
        "url": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "category": "world"
    },
    {
        "name": "Al Jazeera",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "category": "world",
    },
    {
        "name": "NPR News",
        "url": "https://feeds.npr.org/1001/rss.xml",
        "category": "world",
    },
    {
        "name": "Reuters World News",
        "url": "https://www.reutersagency.com/feed/?best-topics=world&post_type=best",
        "category": "world",
    },
    {
        "name": "The Guardian - World",
        "url": "https://www.theguardian.com/world/rss",
        "category": "world",
    },
    {
        "name": "DW News",
        "url": "https://rss.dw.com/rdf/rss-en-all",
        "category": "world",
    },
]

REQUEST_TIMEOUT_SECONDS = 10

USER_AGENT = "Mozilla/5.0 (compatible; NewsNarrationBot/0.1; study project)"

MAX_ARTICLES_PER_SOURCE = 5