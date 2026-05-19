from fastapi import APIRouter

from app.graph.builder import build_graph
from fastapi import Depends

from sqlalchemy.orm import Session

from app.api.dependencies import get_db

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
router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

@router.get("/clients")
async def fetch_clients():

    clients = await list_clients()

    return {
        "clients": clients
    }

@router.post(
    "/advisory/run/{client_id}"
)
async def run_advisory_analysis(
    client_id: str
):
    try:
        result = await run_advisory_workflow(
            client_id
        )

        return result

    except Exception as error:

        return {
            "status": "failed",
            "error": str(error)
        }

@router.post("/workflow/start")
async def start_workflow():

    graph = build_graph()

    initial_state = {
        "client_data": {},
        "analysis": {},
        "logs": []
    }

    result = await graph.ainvoke(
        initial_state
    )

    return result

@router.post("/clients/mock")

async def ingest_mock_client(
    db: Session = Depends(get_db)
):

    payload = generate_mock_client()

    client = await create_client(
        db,
        payload
    )

    return {
        "message": "Mock client created",
        "client_id": client.client_id
    }