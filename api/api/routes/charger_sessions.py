from api.db.db import get_session
from api.models.charger_session import ChargerSessionModel
from api.db.repository import ChargerSessionRepository
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
async def get_all() -> list[ChargerSessionModel]:
    """Get all charger sessions.

    :return: a list charger session models.
    """
    charger_sessions = []
    async with get_session() as session:
        repo = ChargerSessionRepository(session)
        charger_sessions = await repo.get_all()

    return charger_sessions
