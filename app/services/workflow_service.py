from app.graph.orchestrator import (
    build_workflow
)


async def run_advisory_workflow(
    client_id: str
):

    workflow = build_workflow()

    initial_state = {
        "client_id": client_id,

        "client_profile": {},

        "transactions": [],

        "investments": [],

        "portfolio_analysis": {},

        "risk_assessment": {},

        "anomalies": [],

        "advisory_report": {},

        "next_step": "",

        "execution_logs": []
    }

    result = await workflow.ainvoke(
        initial_state
    )

    return result