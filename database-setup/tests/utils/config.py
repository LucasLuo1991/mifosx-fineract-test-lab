import os
from dataclasses import dataclass

from utils.urls import build_fineract_api_base_url, derive_server_url_from_api_base_url


@dataclass
class FineractTestConfig:
    """Runtime configuration for database and Fineract API test access."""

    db_username: str
    db_password: str
    db_endpoint: str
    server_url: str
    api_base_url: str
    api_username: str
    api_password: str
    tenant_id: str


def load_config_from_env() -> FineractTestConfig:
    """Build test configuration from environment variables and local defaults."""
    explicit_api_base_url = os.getenv("API_BASE_URL")
    explicit_server_url = os.getenv("SERVER_URL")
    fineract_port = os.getenv("FINERACT_PORT", "3000")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    default_db_name = os.getenv("FINERACT_TENANT_DEFAULT_DB_NAME", "fineract_default")

    if explicit_api_base_url:
        api_base_url = explicit_api_base_url.rstrip("/")
        server_url = (
            explicit_server_url.rstrip("/")
            if explicit_server_url
            else derive_server_url_from_api_base_url(api_base_url)
        )
    else:
        server_url = (explicit_server_url or f"http://localhost:{fineract_port}").rstrip("/")
        api_base_url = build_fineract_api_base_url(server_url)

    return FineractTestConfig(
        db_username=os.getenv("FINERACT_DB_USER", "postgres"),
        db_password=os.getenv("FINERACT_DB_PASS", "your_secure_password_here"),
        db_endpoint=os.getenv(
            "DB_ENDPOINT", f"localhost:{postgres_port}/{default_db_name}"
        ),
        server_url=server_url,
        api_base_url=api_base_url,
        api_username=os.getenv("API_USER", "mifos"),
        api_password=os.getenv("API_PASS", "password"),
        tenant_id=os.getenv("TENANT_ID", "default"),
    )
