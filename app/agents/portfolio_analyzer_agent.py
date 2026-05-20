from langchain_core.messages import SystemMessage, HumanMessage

from app.services.logging_service import logger
from app.schemas.portfolio_schema import PortfolioAnalysisSchema
from app.services.llm_service import LLMService


# Base singleton LLM
base_llm = LLMService.get_llm()

# Structured output wrapper
structured_llm = base_llm.with_structured_output(
    PortfolioAnalysisSchema
)

async def portfolio_analyzer_agent(state):

    try:

        client_profile = state.get(
            "client_profile",
            {}
        )

        transactions = state.get(
            "transactions",
            []
        )

        investments = state.get(
            "investments",
            []
        )

        if not client_profile:

            logger.warning(
                "Portfolio analyzer received empty client_profile"
            )

            return {
                "portfolio_analysis": {},
                "errors": state.get("errors", []) + [
                    "No client profile data available for analysis"
                ]
            }

        logger.info(
            "Starting portfolio analysis"
        )

        system_prompt = """
        You are an expert financial portfolio analyst.

        Analyze the client's financial profile.

        You MUST provide:
        - investment profile
        - liquidity assessment
        - debt exposure
        - diversification score
        - overall risk level
        - savings ratio (0 to 1)
        - debt to income ratio
        - key insights

        Ensure numeric fields are valid numbers.

        Return structured output only.
        """

        human_prompt = f"""
        Analyze the following client financial data.

        Client Profile:
        {client_profile}

        Transaction History:
        {transactions}

        Investment Portfolio:
        {investments}

        CRM Context:
        {state.get("crm_profile", {})}

        Market Context:
        {state.get("market_context", {})}
        """

        response = await structured_llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])

        logger.info(
            "Portfolio analysis completed successfully"
        )

        return {
            "portfolio_analysis": response.model_dump(),
            "errors": state.get("errors", [])
        }

    except Exception as e:

        logger.error(
            f"Portfolio analyzer failed: {str(e)}",
            exc_info=True
        )

        return {
            "portfolio_analysis": {},
            "errors": state.get("errors", []) + [str(e)]
        }