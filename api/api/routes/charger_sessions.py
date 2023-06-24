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


@router.get("/{id}")
async def get(id: int) -> ChargerSessionModel:
    """Get a charger session by ID.

    :param id: ID of the charger session to get.
    :return: a charger session.
    :raise: if no charger session with the specified id is found, a 404 error is
    raised. 
    """
    charger_session = None
    async with get_session() as session:
        repo = ChargerSessionRepository(session)
        charger_session = await repo.get(id)

    if not charger_session:
        raise HTTPException(status_code=404, detail="Charger session not found.")
    return charger_session
