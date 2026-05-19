from app.services.logging_service import logger


async def risk_evaluator_agent(state):

    logger.info(
        "Evaluating client risk profile"
    )

    analysis = state["portfolio_analysis"]

    risk_level = "LOW"

    if analysis["savings_ratio"] < 0.2:
        risk_level = "HIGH"

    elif analysis["savings_ratio"] < 0.4:
        risk_level = "MEDIUM"

    state["risk_assessment"] = {
        "risk_level": risk_level
    }

    state["execution_logs"].append(
        "Risk evaluation completed"
    )

    return state