from fastapi import FastAPI

from app.api.routes import router
from app.config.settings import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)

app.include_router(router)