DEFAULT_API_PATH = "/fineract-provider/api/v1"
DEFAULT_HEALTH_PATH = "/fineract-provider/actuator/health"


def build_fineract_api_base_url(
    server_url: str, api_path: str = DEFAULT_API_PATH
) -> str:
    """Return a Fineract API base URL from either a server or API URL."""
    server_url = server_url.rstrip("/")
    if server_url.endswith(api_path):
        return server_url
    return f"{server_url}{api_path}"


def derive_server_url_from_api_base_url(
    api_base_url: str, api_path: str = DEFAULT_API_PATH
) -> str:
    """Return the server root URL for a Fineract API base URL."""
    api_base_url = api_base_url.rstrip("/")
    if api_base_url.endswith(api_path):
        return api_base_url[: -len(api_path)]
    return api_base_url


def build_postgres_dsn(username: str, password: str, endpoint: str) -> str:
    """Build a SQLAlchemy PostgreSQL DSN for the Fineract database."""
    return f"postgresql+psycopg://{username}:{password}@{endpoint}"


def build_fineract_health_url(
    server_url: str, health_path: str = DEFAULT_HEALTH_PATH
) -> str:
    """Return a Fineract actuator health URL from a server or health URL."""
    server_url = server_url.rstrip("/")
    if server_url.endswith(health_path):
        return server_url
    return f"{server_url}{health_path}"
