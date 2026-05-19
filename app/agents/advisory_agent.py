from app.services.logging_service import logger


async def advisory_agent(state):

    logger.info(
        "Generating advisory report"
    )

    risk_level = (
        state["risk_assessment"]
        ["risk_level"]
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