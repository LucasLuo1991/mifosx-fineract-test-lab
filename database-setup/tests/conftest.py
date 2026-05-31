from pathlib import Path
from typing import Generator

import pytest
from api.api_client import FineractApiClient
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import Connection
from utils.config import FineractTestConfig, load_config_from_env
from utils.health import wait_for_health_check
from utils.urls import build_fineract_health_url, build_postgres_dsn

load_dotenv(dotenv_path=Path(__file__).parents[2] / ".env")


@pytest.fixture(scope="session")
def config() -> FineractTestConfig:
    """Return test configuration loaded from environment variables."""
    return load_config_from_env()


@pytest.fixture(scope="session", autouse=True)
def wait_for_service_healthy(config: FineractTestConfig) -> None:
    """Stop the test session early if the Fineract health check never becomes ready."""
    try:
        wait_for_health_check(build_fineract_health_url(config.server_url))
    except TimeoutError as error:
        pytest.exit(str(error))


@pytest.fixture(scope="session")
def db_engine(config: FineractTestConfig) -> Generator[Engine, None, None]:
    """Create a session-scoped SQLAlchemy engine for the Fineract database."""
    engine = create_engine(
        build_postgres_dsn(config.db_username, config.db_password, config.db_endpoint)
    )
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(scope="function")
def db_connection(db_engine: Engine) -> Generator[Connection, None, None]:
    """Yield a database connection wrapped in a rollback-only transaction."""
    with db_engine.connect() as connection:
        transaction = connection.begin()
        try:
            yield connection
        finally:
            if transaction.is_active:
                transaction.rollback()


@pytest.fixture(scope="session")
def authenticated_api_client(
    config: FineractTestConfig,
) -> Generator[FineractApiClient, None, None]:
    """Yield an authenticated Fineract API client for endpoint tests."""
    client = FineractApiClient(
        api_base_url=config.api_base_url,
        tenant_id=config.tenant_id,
        api_username=config.api_username,
        api_password=config.api_password,
    )
    client.authenticate()
    try:
        yield client
    finally:
        client.close()
