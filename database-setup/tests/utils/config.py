import os
from dataclasses import dataclass

from utils.urls import build_fineract_api_base_url


@dataclass
class FineractTestConfig:
    db_username: str
    db_password: str
    db_endpoint: str
    api_base_url: str
    api_username: str
    api_password: str
    tenant_id: str


def load_config_from_env() -> FineractTestConfig:
    explicit_api_base_url = os.getenv("API_BASE_URL")
    if explicit_api_base_url:
        api_base_url = explicit_api_base_url.rstrip("/")
    else:
        server_url = os.getenv("SERVER_URL", "http://localhost:3000").rstrip("/")
        api_base_url = build_fineract_api_base_url(server_url)

    return FineractTestConfig(
        db_username=os.getenv("FINERACT_DB_USER", "postgres"),
        db_password=os.getenv("FINERACT_DB_PASS", "your_secure_password_here"),
        db_endpoint=os.getenv("DEFAULT_DB_ENDPOINT", "localhost:5432/fineract_default"),
        api_base_url=api_base_url,
        api_username=os.getenv("API_USER", "mifos"),
        api_password=os.getenv("API_PASS", "password"),
        tenant_id=os.getenv("TENANT_ID", "default"),
    )
