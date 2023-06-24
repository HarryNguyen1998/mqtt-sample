from fastapi import APIRouter, HTTPException
from src.db.db import get_session
from src.models.charger_session import ChargerSessionModel
from src.repository import ChargerSessionRepository

router = APIRouter()


@router.get("/")
async def get_all() -> list[ChargerSessionModel]:
    charger_sessions = []
    async with get_session() as session:
        repo = ChargerSessionRepository(session)
        charger_sessions = await repo.get_all()

    return charger_sessions


@router.get("/{id}")
async def get(id: int) -> ChargerSessionModel:
    charger_session = None
    async with get_session() as session:
        repo = ChargerSessionRepository(session)
        charger_session = await repo.get(id)

    if not charger_session:
        raise HTTPException(status_code=404, detail="Charger session not found.")
    return charger_session
