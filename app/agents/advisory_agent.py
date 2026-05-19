from app.services.logging_service import logger


async def advisory_agent(state):

    logger.info(
        "Generating advisory report"
    )

    risk_assessment = state.get(
    "risk_assessment",
    {}
    )
    market_context = (
    state["market_context"]
    )

    risk_level = risk_assessment.get(
        "risk_level",
        "LOW"
    )

    recommendations = []

    if risk_level == "HIGH":

        recommendations.append(
            "Reduce discretionary spending"
        )

        recommendations.append(
            "Increase emergency savings"
        )

    else:

        recommendations.append(
            "Maintain current investment strategy"
        )
    if (
    market_context[
        "market_sentiment"
    ] == "bearish"
    ):

        recommendations.append(
            "Limit high-risk equity exposure during current market conditions"
        )
    state["advisory_report"] = {
        "risk_level": risk_level,
        "recommendations": recommendations,
        "anomaly_count": len(
            state["anomalies"]
        )
    }

    state["execution_logs"].append(
        "Advisory report generated"
    )

    return state