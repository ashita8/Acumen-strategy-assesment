from pathlib import Path

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

from app.agents.orchestrator_agent import (
    orchestrator_agent
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


def route_workflow(state):

    return state["next_step"]


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
        "orchestrator_agent",
        orchestrator_agent
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
        "orchestrator_agent"
    )

    
    workflow.add_conditional_edges(
    "orchestrator_agent",

    lambda state: state["next_step"],

    {
        "risk_evaluator_agent": "risk_evaluator_agent",

        "advisory_agent": "advisory_agent"
    }
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

    compiled_workflow = workflow.compile()
    graph_png = compiled_workflow.get_graph(xray=True).draw_mermaid_png()

    with open("agent_workflow.png", "wb") as f:
        f.write(graph_png)

    print("Saved")
    save_workflow_image(
        compiled_workflow
    )

    return compiled_workflow


def save_workflow_image(workflow):
    print("******************************")
    docs_path = Path("docs")

    docs_path.mkdir(
        exist_ok=True
    )

    image_bytes = (
        workflow.get_graph()
        .draw_mermaid_png()
    )

    output_path = (
        docs_path / "workflow.png"
    )

    with open(output_path, "wb") as file:

        file.write(image_bytes)