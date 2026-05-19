from langgraph.graph import START, END, StateGraph

from app.agents.data_fetcher import (
    data_fetcher_agent
)

from app.agents.analyzer import (
    analyzer_agent
)

from app.graph.state import AgentState


def build_graph():

    graph_builder = StateGraph(
        AgentState
    )

    graph_builder.add_node(
        "data_fetcher",
        data_fetcher_agent
    )

    graph_builder.add_node(
        "analyzer",
        analyzer_agent
    )

    graph_builder.add_edge(
        START,
        "data_fetcher"
    )

    graph_builder.add_edge(
        "data_fetcher",
        "analyzer"
    )

    graph_builder.add_edge(
        "analyzer",
        END
    )

    return graph_builder.compile()