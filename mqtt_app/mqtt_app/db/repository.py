from mqtt_app.db.orm import ChargerSessionOrm
from mqtt_app.models.charger_session import ChargerSessionModel
from sqlalchemy.orm import Session


class ChargerSessionRepository:
    def __init__(self, session: Session):
        self._session = session

    def create_charger_session(self, charger_session: ChargerSessionModel):
        charger_session_orm = ChargerSessionOrm(**charger_session.dict(by_alias=True))
        self._session.add(charger_session_orm)

        try:
            self._session.commit()
        except Exception as ex:
            self._session.rollback()
            raise ex

        return charger_session_orm
