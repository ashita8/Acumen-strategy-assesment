from app.services.logging_service import logger


async def portfolio_analyzer_agent(state):

    logger.info(
        "Analyzing financial portfolio"
    )

    profile = state["client_profile"]

    income = profile["monthly_income"]

    expenses = profile["monthly_expenses"]

    savings_ratio = (
        (income - expenses) / income
    )

    total_investments = sum(
        investment["current_value"]
        for investment in state["investments"]
    )

    state["portfolio_analysis"] = {
        "savings_ratio": round(
            savings_ratio,
            2
        ),
        "total_investments": total_investments
    }

    state["execution_logs"].append(
        "Portfolio analysis completed"
    )

    return state