from app.services.logging_service import logger


async def data_fetcher_agent(state):

    logger.info("Fetching client data")

    client_data = {
        "client_id": "CL-1001",
        "name": "John Doe",
        "monthly_income": 120000,
        "monthly_expenses": 95000,
        "savings": 200000,
        "investments": 150000
    }

    state["client_data"] = client_data

    state["logs"].append(
        "Client financial data fetched"
    )

    return state