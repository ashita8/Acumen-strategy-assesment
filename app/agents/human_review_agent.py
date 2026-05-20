from langgraph.types import interrupt

from app.services.logging_service import (
    logger
)

from app.services.workflow_session_service import (
    update_workflow_status
)

async def human_review_agent(
    state,
    config
):

    logger.info(
        "Human review required"
    )

    thread_id = (
        config["configurable"][
            "thread_id"
        ]
    )

    logger.info(
        f"thread_id_in_state="
        f"{thread_id}"
    )

    # =========================================
    # UPDATE DB BEFORE INTERRUPT
    # =========================================

    update_workflow_status(

        thread_id=thread_id,

        status="interrupted"
    )

    logger.info(
        "workflow status updated "
        "to interrupted"
    )

    review_payload = {

        "client_id":
            state["client_profile"]["client_id"],

        "risk_level":
            state["portfolio_analysis"][
                "overall_risk_level"
            ],

        "anomalies":
            state["anomalies"],

        "risk_assessment":
            state["risk_assessment"],

        "message":
            "Manual advisor approval required"
    }

    logger.info(
        "ABOUT TO INTERRUPT WORKFLOW"
    )

    approval = interrupt(
        review_payload
    )

    logger.info(
        "WORKFLOW RESUMED"
    )

    state["human_review_response"] = (
        approval
    )

    approved = approval.get(
        "approved",
        False
    )

    if approved:

        state["execution_logs"].append(
            "Human review approved"
        )

        state["next_step"] = (
            "advisory_agent"
        )

    else:

        state["execution_logs"].append(
            "Human review rejected"
        )

        state["next_step"] = (
            "rejected"
        )

    return state