from sqlmodel import Session, create_engine

from src.settings.db import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    session = Session(engine)
    try:
        yield session
    except Exception:
        # ログは例外が箇所で出力する
        session.rollback()
        raise
    finally:
        session.close()
