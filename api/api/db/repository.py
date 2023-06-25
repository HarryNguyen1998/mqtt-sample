from api.db.orm import ChargerSessionOrm
from api.models.charger_session import ChargerSessionModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class ChargerSessionRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[ChargerSessionModel]:
        """Get all charger sessions.

        :return: list of charger session models.
        """
        query = select(ChargerSessionOrm)
        db_models = await self._session.execute(query)
        db_models = db_models.scalars().all()
        models = [ChargerSessionModel.from_orm(db_model) for db_model in db_models]
        return models
