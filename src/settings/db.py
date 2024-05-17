import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

from src.settings.logger import logger

load_dotenv()


def get_env_variable(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        error_message = f"Environment variable {name} not set."
        logger.error(error_message)
        raise EnvironmentError(error_message)
    return value


DB_USERNAME = get_env_variable("DB_USERNAME")
DB_PASSWORD = get_env_variable("DB_PASSWORD")
DB_HOST = get_env_variable("DB_HOST")
DB_DATABASE = get_env_variable("DB_DATABASE")

DATABASE_URL = (
    f"mysql+pymysql://{quote_plus(DB_USERNAME)}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}/{DB_DATABASE}"
)

engine = create_engine(DATABASE_URL, echo=False)


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
