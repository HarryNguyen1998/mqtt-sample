from collections.abc import Generator
from contextlib import contextmanager

from mqtt_app.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = Config.DB_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"connect_timeout": 10})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get a DB session that will close automatically when it's out of scope."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
