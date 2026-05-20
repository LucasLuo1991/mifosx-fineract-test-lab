DEFAULT_API_PATH = "/fineract-provider/api/v1"


def build_fineract_api_base_url(
    server_url: str, api_path: str = DEFAULT_API_PATH
) -> str:
    server_url = server_url.rstrip("/")
    if server_url.endswith(api_path):
        return server_url
    return f"{server_url}{api_path}"


def build_postgres_dsn(username: str, password: str, endpoint: str) -> str:
    return f"postgresql+psycopg://{username}:{password}@{endpoint}"
