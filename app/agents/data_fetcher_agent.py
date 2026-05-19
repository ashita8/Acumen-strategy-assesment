from app.services.logging_service import logger

from app.tools.client_data_tool import (
    fetch_client_financial_data
)
from app.tools.crm_tool import (
    fetch_crm_profile
)

async def data_fetcher_agent(state):

    logger.info(
        "Fetching client financial data"
    )

    financial_data = (
        await fetch_client_financial_data(
            state["client_id"]
        )
    )

    if not financial_data:

        raise ValueError(
            "Client data not found"
        )
    
    crm_profile = await fetch_crm_profile(
    state["client_id"]
    )

    state["crm_profile"] = crm_profile

    state["client_profile"] = (
        financial_data["client_profile"]
    )

    state["transactions"] = (
        financial_data["transactions"]
    )

    state["investments"] = (
        financial_data["investments"]
    )

    state["execution_logs"].append(
        "Client financial data fetched"
    )

    return state