from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from app.services.logging_service import logger

from app.schemas.orchestrator_schema import (
    OrchestratorDecisionSchema
)

from app.services.llm_service import (
    LLMService
)


# =========================================================
# Base LLM
# =========================================================

base_llm = LLMService.get_llm()

structured_llm = (
    base_llm.with_structured_output(
        OrchestratorDecisionSchema
    )
)


# =========================================================
# Orchestrator Agent
# =========================================================

async def orchestrator_agent(state):

    try:

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

        # =================================================
        # System Prompt
        # =================================================

        system_prompt = """
        You are an intelligent workflow orchestrator
        for a financial wealth advisory system.

        Your task is to decide whether the workflow
        should:

        1. Perform deeper risk evaluation
        OR
        2. Generate advisory directly

        Risk evaluation should be triggered for:
        - high debt exposure
        - low liquidity
        - aggressive investment behavior
        - bearish market conditions
        - high market volatility
        - unusually risky portfolios

        Allowed next_step values:
        - risk_evaluator
        - advisory_agent

        Return structured output only.
        """

        # =================================================
        # Human Prompt
        # =================================================

        human_prompt = f"""
        Analyze the following financial context.

        Portfolio Analysis:
        {analysis}

        CRM Profile:
        {crm_profile}

        Market Context:
        {market_context}
        """

        # =================================================
        # LLM Decision
        # =================================================

        response = await structured_llm.ainvoke([

            SystemMessage(
                content=system_prompt
            ),

            HumanMessage(
                content=human_prompt
            )
        ])

        next_step = response.next_step

        state["next_step"] = next_step

        state["execution_logs"].append(

            f"LLM routing decision: "
            f"{response.reasoning}"
        )

        logger.info(
            f"Workflow routed to: {next_step}"
        )

        return state

    except Exception as e:

        logger.error(
            f"Orchestrator failed: {str(e)}",
            exc_info=True
        )

        state["next_step"] = (
            "advisory_agent"
        )

        state["errors"].append(
            str(e)
        )

        return state