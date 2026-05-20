from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router

import app.graph.checkpointer as cp


@asynccontextmanager
async def lifespan(app: FastAPI):

    cp.checkpointer = (
        await cp.checkpointer_cm.__aenter__()
    )

    await cp.checkpointer.setup()

    yield

    await cp.checkpointer_cm.__aexit__(
        None,
        None,
        None
    )


app = FastAPI(
    lifespan=lifespan
)

app.include_router(router)