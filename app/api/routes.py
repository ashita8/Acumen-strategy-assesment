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
router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy"
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