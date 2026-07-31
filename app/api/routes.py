from fastapi import APIRouter

from app.core.logging import logger

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Check"}


@router.get("/health")
def health_check():
    logger.info("Health check requested")

    return {"status": "healthy", "version": "0.1.0"}
