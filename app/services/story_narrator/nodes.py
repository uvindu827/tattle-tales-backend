import logging

from langgraph.types import interrupt

from .State import NarrationSessionState
from .text_to_speech import synthesis_Speech
from .explanation import create_explanation

logger = logging.getLogger(__name__)

def narrate_segment_node(state: NarrationSessionState) -> dict:

    segment = state["segments"][state["current_segment_idx"]]
    is_last_segment = segment["idx"] == state["total_segments"] - 1

    audio_path = f"data/audio/{state['script_id']}_{segment['idx']}.mp3"
    synthesis_Speech(segment["text"], audio_path)

    pending_payload = {
        "type": "segment",
        "segment_idx": segment["idx"],
        "text": segment["text"],
        "audio_path": audio_path,
        "is_last_segment": is_last_segment,
    }

    while True:
        decision = interrupt(pending_payload)

        action = decision.get("action", "continue")

        if action == "question":
            question = decision.get("question", "")
            logger.info("Handling interrupt question: %s", question)

            explanation = create_explanation(question)

            pending_payload = {
                "type": "explanation",
                "question": explanation.question,
                "answer": explanation.answer_text,
                "source_title": explanation.source_title,
                "source_url": explanation.source_url,
            }

            continue

        else:
            break

    next_idx = state["current_segment_idx"] + 1
    is_finished = next_idx >= state["total_segments"]

    return {
        "current_segment_idx": next_idx,
        "is_finished": is_finished,
        "last_audio_path": audio_path,
        "last_explanation": None,
    }