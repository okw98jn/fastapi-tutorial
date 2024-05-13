from sqlmodel import Session
from fastapi import Depends
from src.connector.db_connect import get_session


class BaseService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
