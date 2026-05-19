from app.services.logging_service import logger

from app.tools.client_data_tool import (
    fetch_client_financial_data
)
from app.tools.crm_tool import (
    fetch_crm_profile
)
from app.tools.market_context_tool import (
    fetch_market_context
)
from app.utils.error_utils import (
    append_workflow_error
)

async def data_fetcher_agent(state):

    try:

        financial_data = (
            await fetch_client_financial_data(
                state["client_id"]
            )
        )

        if not financial_data:

            raise ValueError(
                "Client financial data not found"
            )

        crm_profile = await fetch_crm_profile(
            state["client_id"]
        )

        if not crm_profile:

            crm_profile = {
                "risk_appetite": "moderate",
                "client_segment": "retail",
                "investment_goal":
                    "wealth_growth",
                "relationship_years": 0,
                "credit_score": 650,
                "advisor_notes":
                    "Fallback CRM profile"
            }

            state["execution_logs"].append(
                "Fallback CRM profile applied"
            )

        try:

            market_context = (
                await fetch_market_context()
            )

        except Exception:

            market_context = {
                "market_sentiment":
                    "neutral",

                "inflation_rate": 4.0,

                "interest_rate": 5.0,

                "market_volatility":
                    "medium",

                "equity_outlook":
                    "uncertain"
            }

            state["execution_logs"].append(
                "Fallback market context applied"
            )

        state["client_profile"] = (
            financial_data["client_profile"]
        )

        state["transactions"] = (
            financial_data["transactions"]
        )

        state["investments"] = (
            financial_data["investments"]
        )

        state["crm_profile"] = crm_profile

        state["market_context"] = (
            market_context
        )

        state["execution_logs"].append(
            "Client financial data fetched"
        )

        return state

    except Exception as error:

        return append_workflow_error(
            state,
            "data_fetcher_agent",
            str(error)
        )