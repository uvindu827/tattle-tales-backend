from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .State import NarrationSessionState
from .nodes import narrate_segment_node

def _route_after_segment(state: NarrationSessionState) -> str:
    if state["is_finished"]:
        return END

    return "narrate_segment"

def Build_session_graph():
    graph_builder = StateGraph(NarrationSessionState)

    graph_builder.add_node("narrate_segment", narrate_segment_node)
    graph_builder.add_edge(START, "narrate_segment")

    graph_builder.add_conditional_edges(
        "narrate_segment",
        _route_after_segment,
        {"narrate_segment": "narrate_segment", END: END}
    )

    checkpointer = MemorySaver()

    return graph_builder.compile(checkpointer=checkpointer)