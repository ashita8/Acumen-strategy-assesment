from langgraph.types import interrupt

from app.services.logging_service import logger


async def human_review_agent(state):

    logger.info(
        "Human review required"
    )

    review_payload = {

        "client_id":
            state["client_profile"]["client_id"],

        "risk_level":
            state["portfolio_analysis"]["overall_risk_level"],

        "anomalies":
            state["anomalies"],

        "message":
            "Advisor approval required"
    }

    approval = interrupt(review_payload)

    state["human_review"] = approval

    state["execution_logs"].append(
        "Workflow paused for human review"
    )

    return state