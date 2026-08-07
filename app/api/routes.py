from fastapi import APIRouter, Depends

from app.core.logging import logger
from app.dependencies.providers import get_agent_service
from app.schemas.agent import ChatRequest, ChatResponse
from app.services.agent.service import AgentService

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Check"}


@router.get("/health")
def health_check():
    logger.info("Health check requested")

    return {"status": "healthy", "version": "0.1.0"}


@router.post("/agent/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    agent: AgentService = Depends(get_agent_service),  # noqa: B008
):
    response = agent.chat(request.message)

    return ChatResponse(response=response)
