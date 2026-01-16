import os
import pytest
from pathlib import Path
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker

from app.db.session import get_db
from app.main import app

TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5433/health_dashboard_test"

@pytest.fixture(scope="session", autouse=True)
def _migrate_test_db():
    os.environ["DATABASE_URL"]=TEST_DATABASE_URL

    backend_dir = Path(__file__).resolve().parents[1]
    alembic_ini_path = backend_dir / "alembic.ini"

    alembic_cfg = Config(str(alembic_ini_path))

    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)

    command.upgrade(alembic_cfg, "head")

@pytest.fixture(scope="session")
def _engine():
    return create_engine(TEST_DATABASE_URL, pool_pre_ping=True)

@pytest.fixture()
def db_session(_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    db = TestingSessionLocal()

    # Double check we are working with the test db
    current_db = db.execute(text("SELECT current_database();")).scalar_one()
    assert current_db == "health_dashboard_test", f"Refusing to run tests against DB: {current_db}"

    db.execute(text("TRUNCATE TABLE services RESTART IDENTITY CASCADE;"))
    db.commit()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(db_session):
    
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass 
    
    app.dependency_overrides[get_db] = _override_get_db

    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()