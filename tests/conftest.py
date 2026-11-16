import pytest

from app.database import SessionLocal


@pytest.fixture
def db_session():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()