from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Check"}

@router.get("/health")
def health_check():
    return {"status": "healthy", "version": "0.1.0"}
