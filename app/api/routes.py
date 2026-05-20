from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.graph.builder import build_graph

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
    client_id: str
):

    try:

        logger.info(
            f"Starting advisory workflow for "
            f"client_id={client_id}"
        )

        graph = build_graph()

        config = {
            "configurable": {
                "thread_id": (
                    f"{client_id}_wealth_session"
                )
            }
        }

        result = await run_advisory_workflow(
            client_id=client_id,
            graph=graph,
            config=config
        )

        formatted_response = (
            format_final_response(result)
        )

        logger.info(
            f"Workflow completed successfully "
            f"for client_id={client_id}"
        )

        return {
            "status": "success",
            "data": formatted_response
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
            "error": str(error)
        }


# =========================================================
# Create HITL Test Client
# =========================================================

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