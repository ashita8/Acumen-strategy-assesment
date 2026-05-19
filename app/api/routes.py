from fastapi import APIRouter

from app.graph.builder import build_graph

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