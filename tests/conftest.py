from typing import Generator, Any
import subprocess

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.db.models.device import Device
from starlette.testclient import TestClient
from app.db.session import get_db
import os
from app.main import app


test_engine = create_engine(
    "postgresql://postgres_test:postgres_test@localhost:5440/dsh_db_online_test",
    future=True,
)

test_session = sessionmaker(bind=test_engine, expire_on_commit=False)

CLEAN_TABLES = [
    "devices",
]


@pytest.fixture(scope="session", autouse=True)
def run_migration():
    if not os.path.exists("tests/alembic"):
        os.system("alembic init tests/alembic")

    subprocess.run(
        "alembic -c tests/alembic.ini revision --autogenerate -m 'test running migrations'"
    )
    os.system("alembic -c tests/alembic.ini upgrade heads")


@pytest.fixture(scope="function")
def db():
    engine = create_engine(
        "postgresql://postgres_test:postgres_test@localhost:5440/dsh_db_online_test",
        future=True,
    )
    _Session = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)
    session = _Session()
    yield session
    session.close()


@pytest.fixture(scope="function", autouse=True)
def clean_tables(db):
    with db as session:
        with session.begin():
            for table in CLEAN_TABLES:
                session.execute(text(f"""TRUNCATE TABLE {table};"""))


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            with test_session() as session:
                yield session
                session.close()
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def create_device_in_db():
    def wrapper(
        name,
        type_device,
        type_value,
        range_value,
        current_value,
        session: Session,
    ):
        device = Device(
            name=name,
            type_device=type_device,
            type_value=type_value,
            range_value=range_value,
            current_value=current_value,
        )

        with session as db:
            db.add(device)
            db.commit()
            db.flush()

    return wrapper
