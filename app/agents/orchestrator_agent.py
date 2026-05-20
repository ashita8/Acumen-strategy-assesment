from app.services.logging_service import logger


async def orchestrator_agent(state):

    logger.info(
        "Evaluating workflow routing"
    )

    analysis = (
        state["portfolio_analysis"]
    )

    crm_profile = (
        state["crm_profile"]
    )

    market_context = (
        state["market_context"]
    )

    savings_ratio = analysis.get(
    "savings_ratio",
    0.0
    )

    savings_ratio = analysis.get(
    "savings_ratio",
    0.0
)

    risk_appetite = crm_profile.get(
        "risk_appetite",
        "moderate"
    )

    market_sentiment = market_context.get(
        "market_sentiment",
        "neutral"
    )

    market_volatility = market_context.get(
        "market_volatility",
        "medium"
    )
    should_run_risk_analysis = False

    if savings_ratio < 0.3:

        should_run_risk_analysis = True

    if market_volatility == "high":

        should_run_risk_analysis = True

    if (
        risk_appetite == "aggressive"
        and market_sentiment == "bearish"
    ):

        should_run_risk_analysis = True

    if should_run_risk_analysis:

        state["next_step"] = (
            "risk_evaluator_agent"
        )

        state["execution_logs"].append(
            "Routing to risk evaluation workflow"
        )

    else:

        state["next_step"] = (
            "advisory_agent"
        )

        state["execution_logs"].append(
            "Routing directly to advisory workflow"
        )
    if len(state["errors"]) >= 2:

        state["next_step"] = (
            "advisory_agent"
        )

        state["execution_logs"].append(
            "Too many workflow failures detected. Routing directly to advisory."
        )

        return state

    return state