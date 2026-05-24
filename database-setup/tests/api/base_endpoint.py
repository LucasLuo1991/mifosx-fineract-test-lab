from typing import Any

import requests


class BaseEndpoint:
    def __init__(self, session: requests.Session, api_base_url: str, timeout: int = 30):
        self.session = session
        self.api_base_url = api_base_url
        self.timeout = timeout

    def _url(self, endpoint: str) -> str:
        return f"{self.api_base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def _request(
        self, method: str, endpoint: str, expected_status: int, **kwargs: Any
    ) -> requests.Response:
        url = self._url(endpoint)
        try:
            kwargs.setdefault("timeout", self.timeout)
            response = self.session.request(method, url, **kwargs)
            if response.status_code != expected_status:
                raise Exception(
                    f"Expected status {expected_status} but got {response.status_code} for {method} {url}: {response.text}"
                )
            return response
        except requests.RequestException:
            raise

    def _get(self, endpoint: str, expected_status: int = 200, **kwargs: Any) -> Any:
        return self._request("GET", endpoint, expected_status, **kwargs).json()

    def _post(
        self,
        endpoint: str,
        json_body: dict[str, Any],
        expected_status: int = 200,
        expect_json: bool = True,
        **kwargs: Any,
    ) -> Any:
        response = self._request(
            "POST", endpoint, expected_status, json=json_body, **kwargs
        )
        
        if not expect_json:
            if response.text.strip():
                raise Exception(
                    f"Expected empty response but got body for POST {self._url(endpoint)}: {response.text}"
                )
            return None

        return response.json()
