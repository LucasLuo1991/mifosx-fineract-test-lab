import time
from typing import Mapping, cast

import requests


def wait_for_health_check(
    health_url: str,
    max_attempts: int = 10,
    delay_seconds: int = 30,
    timeout_seconds: int = 5,
) -> None:
    """Poll a health endpoint until it reports UP or the retry budget expires."""
    for attempt in range(max_attempts):
        try:
            response = requests.get(health_url, timeout=timeout_seconds)
            if _is_healthy_response(response):
                return
        except (requests.RequestException, ValueError):
            pass

        if attempt < max_attempts - 1:
            time.sleep(delay_seconds)

    raise TimeoutError(f"Service did not become healthy at {health_url}.")


def _is_healthy_response(response: requests.Response) -> bool:
    """Return whether a response is a successful Fineract health payload."""
    if response.status_code != 200:
        return False

    body: object = response.json()
    if not isinstance(body, dict):
        return False

    health_body = cast(Mapping[str, object], body)
    return health_body.get("status") == "UP"
