from langgraph.types import interrupt

from app.services.logging_service import logger


async def human_review_agent(state):

    logger.info(
        "Waiting for human approval"
    )

    approval = interrupt({

        "message":
            "Approve advisory workflow?",

        "portfolio_analysis":
            state["portfolio_analysis"],

        "risk_analysis":
            state.get("risk_analysis")
    })

    state["human_approval"] = approval

    return state