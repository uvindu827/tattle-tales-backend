import logging
import nltk
from nltk.tokenize import sent_tokenize

from .models import NarrationSegment

logger = logging.getLogger(__name__)

def _ensure_punkt_available():
    for resource in ["tokenizers/punkt", "tokenizers/punkt_tab"]:
        try:
            nltk.data.find(resource)
        except:
            resource_name = resource.split("/")[-1]

            logger.info("NLTK resource %s not found locally - downloading it now...", resource_name)
            nltk.download(resource_name, quiet=True)

_ensure_punkt_available()

def split_into_sentences(text: str) -> list[str]:
    if not text or not text.strip():
        return []

    raw_sentences = sent_tokenize(text.strip())

    return [s.strip() for s in raw_sentences if s.strip()]

def build_segments(text: str) -> list[NarrationSegment]:
    sentences = split_into_sentences(text)

    return[
        NarrationSegment(idx=i, text=sentence)
        for i, sentence in enumerate(sentences)
    ]

