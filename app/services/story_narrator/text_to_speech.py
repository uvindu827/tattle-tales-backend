import edge_tts
import asyncio
import logging
import os

logger = logging.getLogger(__name__)

DEFAULT_VOICE = "en-US-AriaNeural"

class TTSError(Exception):
    """
    Custom exception class for TTS errors.
    """

    pass

async def _synthesize_async(text:str, output_path:str, voice:str) -> None:

    communicate = edge_tts.communicate(text, voice)

    await communicate.save(output_path)

def synthesis_Speech(text:str, output_path:str, voice:str = DEFAULT_VOICE) -> str:
    """
    Synthesize the text given to a mp3 and save it in the given output path
    """    

    if not text or not text.strip():
        raise TTSError("Cannot synthesize an empty text")

    parent_dir = os.path.dirname(output_path)

    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    try:
        asyncio.run(_synthesize_async(text, output_path, voice))

    except Exception as e:
        logger.error("TTS synthesis failed: %s", e)

        raise TTSError(f"TTS synthesis failed: {e}") from e

    return output_path