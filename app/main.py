from fastapi import FastAPI

from app.api.routes import router
from app.core.configs import settings
from app.services.logging_service import logger

app = FastAPI(
    title=settings.APP_NAME
)

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting Wealth Advisor AI Service")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Wealth Advisor AI Service")