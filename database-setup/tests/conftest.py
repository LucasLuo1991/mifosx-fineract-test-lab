import os
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

import pytest
import requests
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import Connection

load_dotenv(dotenv_path=Path(__file__).parents[2] / ".env")

DEFAULT_API_PATH = "/fineract-provider/api/v1"
REQUEST_TIMEOUT_SECONDS = 30


@dataclass
class Config:
    db_username: str
    db_password: str
    db_url: str
    api_base_url: str
    api_username: str
    api_password: str
    tenant_id: str


def build_api_base_url() -> str:
    explicit_api_base_url = os.getenv("API_BASE_URL")
    if explicit_api_base_url:
        return explicit_api_base_url.rstrip("/")

    server_url = os.getenv("SERVER_URL", "http://localhost:3000").rstrip("/")
    if server_url.endswith(DEFAULT_API_PATH):
        return server_url

    return f"{server_url}{DEFAULT_API_PATH}"


@pytest.fixture(scope="session")
def config() -> Config:
    return Config(
        db_username=os.getenv("FINERACT_DB_USER", "postgres"),
        db_password=os.getenv("FINERACT_DB_PASS", "your_secure_password_here"),
        db_url=os.getenv("DEFAULT_DB_URL", "localhost:5432/fineract_default"),
        api_base_url=build_api_base_url(),
        api_username=os.getenv("API_USER", "mifos"),
        api_password=os.getenv("API_PASS", "password"),
        tenant_id=os.getenv("TENANT_ID", "default"),
    )


@pytest.fixture(scope="session")
def database_url(config: Config) -> str:
    return f"postgresql+psycopg://{config.db_username}:{config.db_password}@{config.db_url}"


@pytest.fixture(scope="session")
def db_engine(database_url: str) -> Generator[Engine, None, None]:
    engine = create_engine(database_url)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(scope="function")
def db_connection(db_engine: Engine) -> Generator[Connection, None, None]:
    with db_engine.connect() as connection:
        transaction = connection.begin()
        try:
            yield connection
        finally:
            if transaction.is_active:
                transaction.rollback()


@pytest.fixture(scope="session")
def api_session(config: Config) -> Generator[requests.Session, None, None]:
    session = requests.Session()
    try:
        res = session.post(
            f"{config.api_base_url}/authentication",
            headers={"fineract-platform-tenantid": config.tenant_id},
            json={
                "username": config.api_username,
                "password": config.api_password,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        session.close()
        pytest.fail(f"Failed to connect to Fineract API: {exc}")

    if not res.ok:
        session.close()
        pytest.fail(f"Failed to authenticate with API: {res.status_code} - {res.text}")

    try:
        res_json = res.json()
    except requests.JSONDecodeError as exc:
        session.close()
        pytest.fail(f"Failed to parse authentication response as JSON: {exc}")

    if "base64EncodedAuthenticationKey" not in res_json:
        session.close()
        pytest.fail("Failed to authenticate with API: Missing authentication key")

    session.headers.update(
        {
            "fineract-platform-tenantid": config.tenant_id,
            "Authorization": f"Basic {res_json['base64EncodedAuthenticationKey']}",
        }
    )
    try:
        yield session
    finally:
        session.close()
