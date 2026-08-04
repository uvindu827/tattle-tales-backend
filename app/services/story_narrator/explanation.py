import logging

from ...services.common.ollama_client import generate_text, OllamaConnectionError
from .wikipedia_serach import get_wikipedia_summary
from .models import Explanation

logger = logging.getLogger(__name__)

EXPLANATION_SYSTEM_PROMPT = """You are a helpful narrator who was just interrupted by a \
listener asking about something they didn't understand. You will be given the listener's \
question and a Wikipedia extract about the topic. Explain it briefly and clearly, the way \
you'd explain it out loud to a friend who's driving and can't read anything.
 
Strict rules:
- Only use information present in the Wikipedia extract given to you. NEVER invent facts.
- Keep it to 1-3 sentences - just enough to clear up their confusion, not a full lecture.
- Plain spoken sentences only. No bullet points, no headers, no parenthetical asides.
- Get straight to the explanation - don't repeat the question back or say "great question."
"""

FALLBACK_EXTRACT_LENGTH = 300

def _build_explanation_prompt(question:str, wiki_extract:str) -> str:
    return (
        f"The listener asked: \"{question}\"\n\n"
        f"Wikipedia extract:\n{wiki_extract}\n\n"
        f"Now explain this briefly and clearly, following the rules above."
    )

def create_explanation(question:str) -> Explanation:
    wiki_result = get_wikipedia_summary(question)

    if wiki_result is None:
        logger.info("No wikipedia info found for the question: %s", question)

        return Explanation(
            question=question,
            answer_text="I don't have specific information on that but let's continue the story",
            source_title="",
            source_url="",
            found=False,
        )

    prompt = _build_explanation_prompt(question, wiki_result["extract"])

    try:
        answer_text = generate_text(prompt, system=EXPLANATION_SYSTEM_PROMPT)

    except OllamaConnectionError as e:
        logger.warning("LLM unavailable for explanation, falling back to raw extract: %s", e)

        answer_text = wiki_result["extract"][:FALLBACK_EXTRACT_LENGTH]

        if len(wiki_result["extract"]) > FALLBACK_EXTRACT_LENGTH:
            answer_text += "..."

    return Explanation(
        question=question,
        answer_text=answer_text,
        source_title=wiki_result["title"],
        source_url=wiki_result["url"],
        found=True
    )    