from langgraph.graph import (
    START,
    END,
    StateGraph
)

from app.graph.state import (
    AgentState
)

import app.graph.checkpointer as cp

from app.services.logging_service import (
    logger
)

# =========================================================
# Agents
# =========================================================

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

from app.agents.human_review_agent import (
    human_review_agent
)

from app.agents.advisory_agent import (
    advisory_agent
)


# =========================================================
# Build LangGraph Workflow
# =========================================================

def build_graph():

    logger.info(
        "Initializing Wealth Advisor "
        "LangGraph workflow"
    )

    graph_builder = StateGraph(
        AgentState
    )

    # =====================================================
    # Nodes
    # =====================================================

    graph_builder.add_node(
        "data_fetcher",
        data_fetcher_agent
    )

    graph_builder.add_node(
        "portfolio_analyzer",
        portfolio_analyzer_agent
    )

    graph_builder.add_node(
        "orchestrator",
        orchestrator_agent
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
        "human_review",
        human_review_agent
    )

    graph_builder.add_node(
        "advisory_agent",
        advisory_agent
    )

    # =====================================================
    # Core Flow
    # =====================================================

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
        "orchestrator"
    )

    # =====================================================
    # Conditional Routing
    # =====================================================

    graph_builder.add_conditional_edges(

        "orchestrator",

        lambda state: state["next_step"],

        {

            "risk_evaluator":
                "risk_evaluator",

            "advisory_agent":
                "advisory_agent"
        }
    )

    # =====================================================
    # Risk Evaluation Pipeline
    # =====================================================

    graph_builder.add_edge(
        "risk_evaluator",
        "anomaly_detector"
    )

    graph_builder.add_edge(
        "anomaly_detector",
        "human_review"
    )

    graph_builder.add_edge(
        "human_review",
        "advisory_agent"
    )

    # =====================================================
    # Final Output
    # =====================================================

    graph_builder.add_edge(
        "advisory_agent",
        END
    )

    logger.info(
        "LangGraph workflow "
        "compiled successfully"
    )
    compiled_graph = graph_builder.compile(
        checkpointer=cp.checkpointer
    )

    try:

        logger.info(
            "Generating workflow PNG"
        )

        graph_png = (
            compiled_graph
            .get_graph(xray=True)
            .draw_mermaid_png()
        )

        with open(
            "workflow.png",
            "wb"
        ) as f:

            f.write(graph_png)

        logger.info(
            "Workflow PNG generated successfully"
        )

    except Exception as e:

        logger.exception(
            f"PNG generation failed: {str(e)}"
        )

    # =====================================================
    # Compile Graph
    # =====================================================
#     compiled_graph = graph_builder.compile(
#     checkpointer=cp.checkpointer
# )
#     print(compiled_graph.save("compiled_workflow.json"))

#     graph_png = (
#         compiled_graph
#         .get_graph(xray=True)
#         .draw_mermaid_png()
#     )

#     with open("workflow.png", "wb") as f:
#         f.write(graph_png)

     
    
    return compiled_graph
