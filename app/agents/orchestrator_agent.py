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

    savings_ratio = (
        analysis["savings_ratio"]
    )

    risk_appetite = (
        crm_profile["risk_appetite"]
    )

    market_sentiment = (
        market_context[
            "market_sentiment"
        ]
    )

    market_volatility = (
        market_context[
            "market_volatility"
        ]
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

    return state