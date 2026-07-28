from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .state import PipelineState
from .nodes import scrape_node, merge_node, narrate_node

def build_pipeline_graph():
    graph_builder = StateGraph(PipelineState)

    graph_builder.add_node("scrape", scrape_node)
    graph_builder.add_node("merge", merge_node)
    graph_builder.add_node("narrate", narrate_node)

    graph_builder.add_edge(START, "scrape")
    graph_builder.add_edge("scrape", "merge")
    graph_builder.add_edge("merge", "narrate")
    graph_builder.add_edge("narrate", END)

    checkpointer = MemorySaver()

    compiled_graph = graph_builder.compile(checkpointer=checkpointer)

    return compiled_graph


