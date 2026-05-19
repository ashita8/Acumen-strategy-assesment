from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.graph.state import WorkflowState

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


def build_workflow():

    workflow = StateGraph(
        WorkflowState
    )

    workflow.add_node(
        "data_fetcher_agent",
        data_fetcher_agent
    )

    workflow.add_node(
        "portfolio_analyzer_agent",
        portfolio_analyzer_agent
    )

    workflow.add_node(
        "risk_evaluator_agent",
        risk_evaluator_agent
    )

    workflow.add_node(
        "anomaly_detector_agent",
        anomaly_detector_agent
    )

    workflow.add_node(
        "advisory_agent",
        advisory_agent
    )

    workflow.add_edge(
        START,
        "data_fetcher_agent"
    )

    workflow.add_edge(
        "data_fetcher_agent",
        "portfolio_analyzer_agent"
    )

    workflow.add_edge(
        "portfolio_analyzer_agent",
        "risk_evaluator_agent"
    )

    workflow.add_edge(
        "risk_evaluator_agent",
        "anomaly_detector_agent"
    )

    workflow.add_edge(
        "anomaly_detector_agent",
        "advisory_agent"
    )

    workflow.add_edge(
        "advisory_agent",
        END
    )

    return workflow.compile()