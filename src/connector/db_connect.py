from sqlmodel import Session, create_engine

from src.logger import logger
from src.settings.db import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    session = Session(engine)
    try:
        yield session
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
