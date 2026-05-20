from app.services.logging_service import (
    logger
)

from app.services.client_service import (
    fetch_client_data
)


async def run_advisory_workflow(
    client_id: str,
    graph,
    config
):

    logger.info(
        f"Running workflow for "
        f"client_id={client_id}"
    )

    client_data = await fetch_client_data(
        client_id
    )

    initial_state = {

        "client_id": client_id,

        "client_profile": client_data.get(
            "client_profile",
            {}
        ),

        "transactions": client_data.get(
            "transactions",
            []
        ),

        "investments": client_data.get(
            "investments",
            []
        ),

        "portfolio_analysis": {},

        "risk_assessment": {},

        "anomalies": [],

        "advisory_report": {},

        "next_step": None,

        "execution_logs": [],

        "crm_profile": client_data.get(
            "crm_profile",
            {}
        ),

        "market_context": client_data.get(
            "market_context",
            {}
        ),

        "errors": []
    }

    result = await graph.ainvoke(
        initial_state,
        config=config
    )

    return result