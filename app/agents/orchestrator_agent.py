from app.services.logging_service import logger


async def orchestrator_agent(state):

    logger.info(
        "Evaluating workflow routing"
    )

    analysis = state["portfolio_analysis"]

    savings_ratio = (
        analysis["savings_ratio"]
    )

    if savings_ratio < 0.3:

        state["next_step"] = (
            "risk_evaluator_agent"
        )

        state["execution_logs"].append(
            "Routing to risk evaluator"
        )

    else:

        state["next_step"] = (
            "advisory_agent"
        )

        state["execution_logs"].append(
            "Routing directly to advisory"
        )

    return state