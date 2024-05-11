from sqlmodel import create_engine, Session
from src.settings.db import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
