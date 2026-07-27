from app.api.routes import router
from fastapi import FastAPI

app = FastAPI(
    title="LLMOps Platform",
    version="0.1.0",
)

app.include_router(router)