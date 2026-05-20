from langgraph.types import interrupt

from app.services.logging_service import (
    logger
)


async def human_review_agent(state):

    logger.info(
        "Pausing workflow for human review"
    )

    review_payload = {
        "client_id": state.get(
            "client_id"
        ),

        "portfolio_analysis": state.get(
            "portfolio_analysis"
        ),

        "risk_assessment": state.get(
            "risk_assessment"
        ),

        "anomalies": state.get(
            "anomalies"
        )
    }

    human_decision = interrupt(
        {
            "message": (
                "Human approval required"
            ),
            "review_data": review_payload
        }
    )

    logger.info(
        f"Human review completed: "
        f"{human_decision}"
    )

    return {
        "execution_logs": [
            "Human review completed"
        ],

        "human_review_decision":
            human_decision
    }