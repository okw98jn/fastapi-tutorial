from urllib.parse import quote_plus

from sqlmodel import Session, create_engine

from src.utils.environment import get_env_variable

DB_USERNAME = get_env_variable("DB_USERNAME")
DB_PASSWORD = get_env_variable("DB_PASSWORD")
DB_HOST = get_env_variable("DB_HOST")
DB_PORT = get_env_variable("DB_PORT")
DB_DATABASE = get_env_variable("DB_DATABASE")

DATABASE_URL = (
    f"postgresql://{quote_plus(DB_USERNAME)}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    session = Session(engine)
    try:
        yield session
    except Exception:
        # ログは例外発生箇所で出力する
        session.rollback()
        raise
    finally:
        session.close()
