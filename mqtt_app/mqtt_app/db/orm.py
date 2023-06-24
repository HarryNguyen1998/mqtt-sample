from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChargerSessionOrm(Base):
    """ORM mapped charger session."""

    __tablename__ = "charger_sessions"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    energy_delivered_in_kWh = Column(Integer)
    duration_in_seconds = Column(Integer)
    session_cost_in_cents = Column(Integer)
