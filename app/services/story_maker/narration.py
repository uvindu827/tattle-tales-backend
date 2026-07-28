import logging

from ..common.ollama_client import generate_text
from ..news_merger.models import MergedNews
from .segmentation import build_segments
from .models import NarrationScript, now_iso

logger = logging.getLogger(__name__)

NARRATION_SCRIPT_PROMPT = """
You are a warm, clear radio news narrator, writing a script \
that will be read aloud by a text-to-speech voice to someone listening while driving or \
relaxing. Your job is to turn a news summary into natural SPOKEN narration.
 
Strict rules you must follow:
- Only use information present in the summary you are given. NEVER invent or add facts.
- Write in plain, flowing sentences - the way a person would actually SAY something out \
loud, not the way a written article would print it.
- Do NOT use bullet points, numbered lists, headers, or any written-document formatting.
- Do NOT use parenthetical asides or semicolons - break complex ideas into separate, \
simple sentences instead, since that's easier to follow by ear than by eye.
- Naturally mention which sources reported the story (e.g. "according to BBC News and \
Al Jazeera"), woven into the narration itself rather than listed separately.
- Keep it to 2-4 sentences - concise enough to listen to comfortably, without dropping \
any of the core facts from the summary.
"""

def _build_narration_promot(mergedNews: MergedNews) -> str:
    sources_text = ", ".join(mergedNews.source_names)

    return(
        f"Headline: {mergedNews.headline}\n"
        f"Sources: {sources_text}\n"
        f"Summary: {mergedNews.merged_summary}\n\n"
        f"Now write the spoken narration script for this story, following all the rules above."
    )

def generate_narration_text(mergedNews: MergedNews) -> str:
    prompt = _build_narration_promot(mergedNews)
    return generate_text(prompt, system=NARRATION_SCRIPT_PROMPT)

def create_narration_script(mergedNews: MergedNews) -> NarrationScript:
    logger.info("Generating narration for: %s", mergedNews.headline)

    narration_text = generate_narration_text(mergedNews)
    segments = build_segments(narration_text)

    return NarrationScript(
        id=mergedNews.id,
        headline=mergedNews.headline,
        category=mergedNews.category,
        source_names=mergedNews.source_names,
        segments=segments,
        created_at=now_iso(),
    )