from app.services.logging_service import logger


async def analyzer_agent(state):

    logger.info("Analyzing client financial data")

    client_data = state["client_data"]

    income = client_data["monthly_income"]
    expenses = client_data["monthly_expenses"]

    savings_ratio = (
        (income - expenses) / income
    )

    risk_level = "LOW"

    if savings_ratio < 0.2:
        risk_level = "HIGH"

    analysis = {
        "savings_ratio": round(savings_ratio, 2),
        "risk_level": risk_level
    }

    state["analysis"] = analysis

    state["logs"].append(
        "Financial analysis completed"
    )

    return state