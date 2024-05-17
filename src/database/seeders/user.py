from sqlmodel import Session

from src.models.user import User
from src.settings.db import engine

with Session(engine) as session:
    users = [
        User(
            name=f"テストユーザー {i+1}",
            email=f"test{i+1}@example.com",
            password="1234",
        )
        for i in range(10000)
    ]
    session.bulk_save_objects(users)
    session.commit()
