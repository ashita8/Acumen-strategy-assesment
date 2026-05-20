from langgraph.graph import START, END, StateGraph

from app.graph.state import AgentState

from app.agents.data_fetcher_agent import (
    data_fetcher_agent
)

from app.agents.portfolio_analyzer_agent import (
    portfolio_analyzer_agent
)

from app.agents.risk_evaluator_agent import (
    risk_evaluator_agent
)

from app.agents.anomaly_detector_agent import (
    anomaly_detector_agent
)

from app.agents.advisory_agent import (
    advisory_agent
)

from app.services.logging_service import logger


def build_graph():

    logger.info(
        "Initializing Wealth Advisor LangGraph workflow"
    )

    graph_builder = StateGraph(
        AgentState
    )

    graph_builder.add_node(
        "data_fetcher",
        data_fetcher_agent
    )

    graph_builder.add_node(
        "portfolio_analyzer",
        portfolio_analyzer_agent
    )

    graph_builder.add_node(
        "risk_evaluator",
        risk_evaluator_agent
    )

    graph_builder.add_node(
        "anomaly_detector",
        anomaly_detector_agent
    )

    graph_builder.add_node(
        "advisory_agent",
        advisory_agent
    )

    graph_builder.add_edge(
        START,
        "data_fetcher"
    )

    graph_builder.add_edge(
        "data_fetcher",
        "portfolio_analyzer"
    )

    graph_builder.add_edge(
        "portfolio_analyzer",
        "risk_evaluator"
    )

    graph_builder.add_edge(
        "risk_evaluator",
        "anomaly_detector"
    )

    graph_builder.add_edge(
        "anomaly_detector",
        "advisory_agent"
    )

    graph_builder.add_edge(
        "advisory_agent",
        END
    )

    logger.info(
        "LangGraph workflow compiled successfully"
    )

    return graph_builder.compile()