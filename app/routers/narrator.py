import os
import uuid
import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from langgraph.types import Command

from ..services.story_narrator.graph import Build_session_graph
from ..services.story_narrator.full_audio import generate_full_audio
from ..services.story_maker.storage import load_existing as load_script
from ..services.story_maker.models import NarrationScript
from ..schemas.narrator_session import StartSessionRequest, AskQuestionRequest, NarratorStepResult, FullAudioResult

logger = logging.getLogger(__name__)

router = APIRouter()

_compiled_graph = Build_session_graph()

def _audio_url(audio_path:str | None) -> str | None:
    if audio_path is None:
        return None

    filename = os.path.basename(audio_path)

    return f"/api/v1/narrate/audio/{filename}"

def _build_step_reslts(thread_id: str, graph_results: dict) -> NarratorStepResult:
    if "__interrupt__" not in graph_results:
        return NarratorStepResult(thread_id = thread_id, finished=True)

    payload = graph_results["__interrupt__"][0].value

    if payload["type"] == "segment":
        return NarratorStepResult(
            thread_id=thread_id,
            finished=True,
            type="segment",
            segment_idx=payload["segment_idx"],
            text=payload["text"],
            audio_url=_audio_url(payload["audio_path"]),
            is_last_segment=payload["is_last_segment"],
        )
    else:
        return NarratorStepResult(
            thread_id=thread_id,
            finished=True,
            type="explanation",
            question=payload["question"],
            answer=payload["answer"],
            source_title=payload["source_title"],
            source_url=payload["source_url"],
        )

@router.post("/narrate/sessions", response_model=NarratorStepResult)
def start_session(request: StartSessionRequest):
    scripts = load_script()
    script_data = scripts.get(request.script_id)

    if script_data is None:
        raise HTTPException(status_code=404, detail=f"Narration script '{request.script_id}' not found")

    script = NarrationScript.from_dict(script_data)

    thread_id = str(uuid.uuid4())

    initial_state = {
        "script_id": script.id,
        "headline": script.headline,
        "source_names": script.source_names,
        "segments": [s.to_dict() for s in script.segments],
        "current_segment_idx": 0,
        "total_segments": len(script.segments),
        "is_finished": False,
        "last_audio_path": None,
        "last_explanation": None,
    }

    config = {"configurable": {"thread_id": thread_id}}

    logger.info("Starting narration session %s for script %s", thread_id, script.id)

    result = _compiled_graph.invoke(initial_state, config)

    return _build_step_reslts(thread_id, result)

@router.post("/narrator/sessions/{thread_id}/continue", response_model=NarratorStepResult)
def continue_session(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}

    result = _compiled_graph.invoke(Command(resume={"action":"continue"}), config)

    return _build_step_reslts(thread_id, result)

@router.post("/narrator/sessions/{thread_id}/ask", response_model=NarratorStepResult)
def ask_question(thread_id: str, request: AskQuestionRequest):
    config = {"configurable": {"thread_id":thread_id}}

    result = _compiled_graph.invoke(
        Command(resume={"action":"question", "question":request.question}),
        config,
    )

    return _build_step_reslts(thread_id, result)

@router.post("/narrator/audio/{filename}", response_model=NarratorStepResult)
def get_audio(filename: str):
    path = os.path.join("data", "audio", filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Audio file '{filename}' not found")

    return FileResponse(path, media_type="audio/mpeg")

@router.post("/narrator/scripts/{script_id}/full-audio", response_model=FullAudioResult)
def get_full_audio(script_id: str):
    scripts = load_script()
    script_data = scripts.get(script_id)

    if script_data is None:
        raise HTTPException(status_code=404, detail=f"Narration script '{script_id}' not found")

    script = NarrationScript.from_dict(script_data)

    audio_path = generate_full_audio(script)

    return FullAudioResult(
        script_id=script_id,
        audio_url=_audio_url(audio_path)
    )