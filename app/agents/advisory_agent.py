from langchain_core.messages import SystemMessage, HumanMessage
from app.services.llm_service import LLMService
from app.services.memory_service import (
    MemoryService
)
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
        #long term memory retrieval
        historical_memories = (
            await MemoryService.get_memories(
                state.get("client_id")
            )
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
        {risk_assessment}

        Anomaly Report:
        {anomaly_report}

        Historical Advisory Insights:
        {historical_memories}
        """

        response = await llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])

        await MemoryService.save_memory(
            client_id=state.get(
                "client_id"
            ),

            memory_type="advisory_summary",

            memory_summary=response.content
        )

        return {
            "advisory_report": response.content,
            "errors": state.get("errors", [])
        }

    except Exception as e:

        return {
            "advisory_report": {},
            "errors": state.get("errors", []) + [str(e)]
        }