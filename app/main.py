from fastapi import FastAPI

from app.api.routes import router
from app.config.settings import settings
from app.core.logging import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)

app.include_router(router)

logger.info(f"Starting {settings.APP_NAME}")
logger.info(f"Environment: {settings.ENVIRONMENT}")
logger.info(f"Version: {settings.VERSION}")
