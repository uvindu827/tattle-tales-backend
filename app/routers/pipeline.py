import uuid
import logging

from fastapi import APIRouter

from ..orchestration.graph import build_pipeline_graph
from ..schemas.pipeline import PipelineResults

logger = logging.getLogger(__name__)

router = APIRouter()

_compiled_graph = build_pipeline_graph()

@router.post("/pipeline/run", response_model=PipelineResults)
def run_pipeline():
    thread_id = str(uuid.uuid4())

    logger.info("Starting full pipeline run, thread_id = %s", thread_id)

    initial_state = {
        "articles_scraped": 0,
        "new_articles": 0,
        "stories_merged": 0,
        "new_stories": 0,
        "scripts_narrated": 0,
        "new_scripts": 0,
        "log": [],
    }

    config = {
        "configurable": {"thread_id": thread_id}
    }

    final_state = _compiled_graph.invoke(initial_state, config)

    return PipelineResults(
        thread_id=thread_id,
        **final_state,
    )