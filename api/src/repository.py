from src.db.orm import ChargerSessionOrm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.charger_session import ChargerSessionModel


class ChargerSessionRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[ChargerSessionModel]:
        """Get all charger sessions."""
        query = select(ChargerSessionOrm)
        db_models = await self._session.execute(query)
        db_models = db_models.scalars().all()
        models = [ChargerSessionModel.from_orm(db_model) for db_model in db_models]
        return models

    async def get(self, session_id: int) -> ChargerSessionModel:
        """Get a charger session given the specified id."""
        query = select(ChargerSessionOrm).where(
            ChargerSessionOrm.session_id == session_id
        )
        db_model = await self._session.execute(query)
        db_model = db_model.scalars().first()
        if not db_model:
            return db_model
        return ChargerSessionModel.from_orm(db_model)
