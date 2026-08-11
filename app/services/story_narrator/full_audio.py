import os
import logging

from .text_to_speech import synthesis_Speech
from ...services.story_maker.models import NarrationScript

logger = logging.getLogger(__name__)

FULL_AUDIO_DIR = os.path.join("data", "audio")

def build_full_narration_script(script:NarrationScript) -> str:
    return " ".join(segment.text for segment in script.segments)

def generate_full_audio(script:NarrationScript, voice:str | None = None) -> str:
    output_path = os.path.join(FULL_AUDIO_DIR, f"{script.id}_full.mp3")

    if os.path.exists(output_path):
        logger.info("Full audio for sript: %s already exists", script.id)

        return output_path

    full_text = build_full_narration_script(script)

    logger.info("Generating full audi for script %s (%d characters)", script.id, len(full_text))

    if voice:
        return synthesis_Speech(full_text, output_path, voice)

    return synthesis_Speech(full_text, output_path)

