import logging

from ..common.ollama_client import generate_text
from .models import MergedNews, now_iso

logger = logging.getLogger(__name__)

SYNTHESIS_PROMPT = """
You are a careful, neutral news editor. You will be given \
several news articles that all report on the SAME real-world event, from different \
sources. Your job is to write ONE clean, consolidated summary of the event.
 
Strict rules you must follow:
- Only use information that is explicitly present in the articles provided.
- NEVER invent, guess, or assume any fact, name, date, or number that isn't stated.
- If the articles disagree on a detail, mention that there is disagreement rather \
than picking one version silently.
- Write in a neutral, factual tone - no editorializing or opinion.
- Keep the summary to one focused paragraph, suitable for being read aloud.
"""

def _build_synthesis_prompt(articles: list[dict]) -> str:
    sections = []

    for i, article in enumerate(articles, start=1):
        excerpt = article["full_text"][:800] if article["full_text"] else article["summary"]
        sections.append(
            f"Article {i} (Source: {article['source']}): \n"
            f"Title: {article['title']}\n"
            f"Content: {excerpt}\n"
        )

        joined_articles = "\n".join(sections)

        return (
            f"Here are {len(articles)} articles about the same event: \n\n"
            f"{joined_articles}\n"
            f"Now write your response in EXACTLY this format, with no extra commentary:\n\n"
            f"HEADLINE: <a single clear headline for this event>\n"
            f"SUMMARY: <one consolidatinng paragraph summarizing what happened>"
        )
    
def _parse_synthesis_prompt(response_text: str, fallback_title: str) -> tuple[str, str]:
    headline = fallback_title
    summary = response_text.strip()

    lines = response_text.strip().split("\n")
    summary_lines = []
    found_summary_marker = False

    for line in lines:
        stripped = line.strip()

        if stripped.upper().startswith("HEADLINE:"):
            headline = stripped[len("HEADLINE:"):].strip()

        elif stripped.upper().startswith("SUMMARY:"):
            found_summary_marker = True
            summary_lines.append(stripped[len("SUMMARY:"):].strip())

        elif found_summary_marker:
            summary_lines.append(stripped)

    if summary_lines:
        summary = " ".join(part for part in summary_lines if part)

    return headline, summary

def synthesize_cluster(articles: list[dict]) -> MergedNews:
    articel_ids = [a["id"] for a in articles]
    source_names = [a["source"] for a in articles]
    published_dates = [a["published_at"] for a in articles if a["published_at"]]

    category = articles[0]["category"]

    if len(articles) == 1:
        logger.info("Cluster only have 1 article: %s. Skipping synthesis", articles[0]["title"])

        headline = articles[0]["title"]
        summary = articles[0]["summary"] or articles["full_text"][:500]

    else:
        logger.info("Synthesizing %d articles in to one merged article", len(articles))

        prompt = _build_synthesis_prompt(articles)
        
        response_text = generate_text(prompt, system=SYNTHESIS_PROMPT)
        headline, summary = _parse_synthesis_prompt(response_text, fallback_title=articles[0]["title"])

    return MergedNews(
            id=MergedNews.make_merged_news_id(articel_ids),
            headline=headline,
            merged_summary=summary,
            source_article_ids=articel_ids,
            source_names=source_names,
            category=category,
            earliest_published=min(published_dates) if published_dates else "",
            latest_published=max(published_dates) if published_dates else "",
            merged_at=now_iso(),
        )   


