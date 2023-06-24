from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def pong():
    """Example route for healthcheck."""
    return {"ping": "pong"}
