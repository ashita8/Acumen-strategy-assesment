from langchain_core.messages import SystemMessage, HumanMessage
from app.services.llm_service import LLMService

llm = LLMService.get_llm()


async def advisory_agent(state):

    try:

        portfolio_analysis = state.get(
            "portfolio_analysis",
            {}
        )

        risk_assessment = state.get(
            "risk_assessment",
            {}
        )

        anomaly_report = state.get(
            "anomaly_report",
            {}
        )

        system_prompt = """
        You are a senior Wealth Advisor Assistant.

        Generate a professional advisory report.

        Include:
        - client portfolio summary
        - risk observations
        - anomaly findings
        - investment recommendations
        - wealth optimization strategies
        - next best actions

        Keep the tone executive and professional.
        """

        human_prompt = f"""
        Portfolio Analysis:
        {portfolio_analysis}

        Risk Analysis:
        {risk_analysis}

        Anomaly Report:
        {anomaly_report}
        """

        response = await llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])

        return {
            "final_response": response.content
        }

    except Exception as e:

        return {
            "final_response": {},
            "errors": state.get("errors", []) + [str(e)]
        }