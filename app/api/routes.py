from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
import uuid
from app.api.dependencies import get_db

from app.graph.builder import build_graph
from langgraph.types import Command
from app.schemas.hitl_schema import (
    HITLResponseSchema
)
from app.services.faker_service import (
    generate_mock_client
)

from app.services.client_service import (
    create_client
)

from app.services.workflow_service import (
    run_advisory_workflow
)
from app.models.crm_profile_model import (
    CRMProfile
)

from app.tools.client_listing_tool import (
    list_clients
)

from app.utils.response_formatter import (
    format_final_response
)

from app.services.logging_service import (
    logger
)

from app.services.workflow_session_service import (

    save_workflow_session,

    get_latest_interrupted_thread_id
)
router = APIRouter()


# =========================================================
# Health Check
# =========================================================

@router.get("/health")
async def health_check():

    return {
        "status": "healthy"
    }


# =========================================================
# List Clients
# =========================================================

@router.get("/clients")
async def fetch_clients():

    try:

        clients = await list_clients()

        return {
            "status": "success",
            "clients": clients
        }

    except Exception as error:

        logger.error(
            f"Failed to fetch clients: {str(error)}",
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# Run Advisory Workflow
# =========================================================

@router.post(
    "/advisory/run/{client_id}"
)
async def run_advisory_analysis(

    client_id: str,

    payload: HITLResponseSchema | None = None
):

    try:

        logger.info(
            f"Starting advisory workflow for "
            f"client_id={client_id}"
        )

        graph = build_graph()

        # =========================================
        # Detect Resume Request
        # =========================================

        is_resume_request = (

            payload is not None

            and

            payload.approved == True
        )

        logger.info(
            f"is_resume_request="
            f"{is_resume_request}"
        )

        # =========================================
        # Resume Interrupted Workflow
        # =========================================

        if is_resume_request:

            logger.info(
                "Fetching interrupted workflow session"
            )

            thread_id = (
                get_latest_interrupted_thread_id(
                    client_id
                )
            )

            if not thread_id:

                return {

                    "status": "failed",

                    "error":
                        "No interrupted workflow found"
                }

            logger.info(
                f"Resuming workflow "
                f"thread_id={thread_id}"
            )

        # =========================================
        # Start Fresh Workflow
        # =========================================

        else:

            logger.info(
                "Creating new workflow session"
            )

            thread_id = str(
                uuid.uuid4()
            )

            save_workflow_session(

                client_id=client_id,

                thread_id=thread_id,

                status="running"
            )

            logger.info(
                f"New workflow session created "
                f"thread_id={thread_id}"
            )

        # =========================================
        # LangGraph Config
        # =========================================

        config = {

            "configurable": {

                "thread_id":
                    thread_id
            }
        }

        # =========================================
        # Resume Existing Workflow
        # =========================================

        if is_resume_request:

            logger.info(
                "Resuming interrupted workflow"
            )

            result = await graph.ainvoke(

                Command(
                    resume={

                        "approved":
                            payload.approved,

                        "advisor_notes":
                            payload.advisor_notes
                    }
                ),

                config=config
            )

        # =========================================
        # Start Fresh Workflow
        # =========================================

        else:

            logger.info(
                "Starting fresh workflow"
            )

            result = await run_advisory_workflow(

                client_id=client_id,

                graph=graph,

                config=config
            )

        # =========================================
        # Fetch Latest Persisted State
        # =========================================

        latest_state = await graph.aget_state(
            config=config
        )
        if latest_state.next:

            return {

                "status": "interrupted",

                "thread_id": thread_id,

                "message":
                    "Human approval required",

                "interrupt_data":
                    latest_state.tasks
            }

        final_state = latest_state.values

        formatted_response = (
            format_final_response(
                final_state
            )
        )

        logger.info(
            f"Workflow completed successfully "
            f"for client_id={client_id}"
        )

        return {

            "status": "success",

            "thread_id":
                thread_id,

            "data":
                formatted_response
        }

    except Exception as error:

        logger.error(
            f"Workflow failed for "
            f"client_id={client_id}: "
            f"{str(error)}",
            exc_info=True
        )

        return {

            "status": "failed",

            "error":
                str(error)
        }
        
@router.post("/clients/hitl")
async def create_hitl_test_client(
    db: Session = Depends(get_db)
):

    try:

        logger.info(
            "Creating HITL test client"
        )

        payload = {

            "client": {

                "client_id":
                    "hitl-test-client",

                "name":
                    "High Risk HITL Client",

                "monthly_income":
                    5000,

                "monthly_expenses":
                    4800,

                "savings_balance":
                    500
            },

            
            "transactions": [

                {
                    "transaction_id": "tx-1",
                    "amount": 1000,
                    "category": "groceries",
                    "transaction_type": "debit"
                },

                {
                    "transaction_id": "tx-2",
                    "amount": 1200,
                    "category": "shopping",
                    "transaction_type": "debit"
                },

                {
                    "transaction_id": "tx-3",
                    "amount": 900,
                    "category": "travel",
                    "transaction_type": "debit"
                },

                {
                    "transaction_id": "tx-4",
                    "amount": 1500,
                    "category": "utilities",
                    "transaction_type": "debit"
                },

                # =====================================
                # Intentional anomaly
                # =====================================

                {
                    "transaction_id": "tx-5",
                    "amount": 250000,
                    "category": "wire_transfer",
                    "transaction_type": "debit"
                }
            ],

            "investments": [

                {
                    "asset_name":
                        "Crypto Futures",

                    "asset_type":
                        "crypto",

                    "current_value":
                        250000
                },

                {
                    "asset_name":
                        "Leveraged Options",

                    "asset_type":
                        "derivatives",

                    "current_value":
                        150000
                }
            ]
        }

        client = await create_client(
            db,
            payload
        )

        # =========================================
        # Create CRM Profile
        # =========================================

        crm_profile = CRMProfile(

            client_id=client.client_id,

            client_segment="HNI",

            risk_appetite="aggressive",

            investment_goal="wealth_growth",

            relationship_years=12,

            credit_score=580,

            advisor_notes=(
                "High-risk leveraged client "
                "requiring manual review"
            )
        )

        db.add(crm_profile)

        db.commit()
        logger.info(
            f"HITL test client created "
            f"client_id={client.client_id}"
        )

        return {

            "status": "success",

            "message":
                "HITL test client created",

            "client_id":
                client.client_id
        }

    except Exception as error:

        logger.error(
            f"HITL client creation failed: "
            f"{str(error)}",
            exc_info=True
        )

        return {
            "status": "failed",
            "error": str(error)
        }