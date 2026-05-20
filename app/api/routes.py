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
# Manual Workflow Trigger
# =========================================================

@router.post("/workflow/start")
async def start_workflow():

    try:

        logger.info(
            "Starting manual workflow"
        )

        graph = build_graph()

        initial_state = {

            "client_id": None,

            "client_profile": {},

            "transactions": [],

            "investments": [],

            "portfolio_analysis": {},

            "risk_assessment": {},

            "anomalies": [],

            "advisory_report": {},

            "next_step": None,

            "execution_logs": [],

            "crm_profile": {},

            "market_context": {},

            "errors": []
        }

        config = {
            "configurable": {
                "thread_id": (
                    "manual_workflow_session"
                )
            }
        }

        result = await graph.ainvoke(
            initial_state,
            config=config
        )

        formatted_response = (
            format_final_response(result)
        )

        return {
            "status": "success",
            "data": formatted_response
        }

    except Exception as error:

        logger.error(
            f"Manual workflow failed: "
            f"{str(error)}",
            exc_info=True
        )

        return {
            "status": "failed",
            "error": str(error)
        }


# =========================================================
# Generate Mock Client
# =========================================================

@router.post("/clients/mock")
async def ingest_mock_client(
    db: Session = Depends(get_db)
):

    try:

        logger.info(
            "Generating mock client"
        )

        payload = generate_mock_client()

        client = await create_client(
            db,
            payload
        )

        logger.info(
            f"Mock client created "
            f"client_id={client.client_id}"
        )

        return {
            "status": "success",
            "message": "Mock client created",
            "client_id": client.client_id
        }

    except Exception as error:

        logger.error(
            f"Mock client creation failed: "
            f"{str(error)}",
            exc_info=True
        )

        return {
            "status": "failed",
            "error": str(error)
        }