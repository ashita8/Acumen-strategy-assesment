from langchain_core.messages import SystemMessage, HumanMessage
from app.services.llm_service import LLMService

llm = LLMService.get_llm()

async def risk_evaluator_agent(state):

    try:

        portfolio_analysis = state.get("portfolio_analysis", {})

        system_prompt = """
        You are a financial risk evaluator.

        Identify:
        - fraud indicators
        - risky transaction patterns
        - compliance concerns
        - abnormal financial behavior

        Return structured JSON.
        """

        human_prompt = f"""
        Portfolio Analysis:

        {portfolio_analysis}
        """

        response = await llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])

        return {
            "risk_assessment": response.content,
            "errors": state.get("errors", [])
        }

    except Exception as e:

        return {
            "risk_assessment": {},
            "errors": state.get("errors", []) + [str(e)]
        }