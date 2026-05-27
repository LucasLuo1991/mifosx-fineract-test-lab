import api.endpoints as endpoints
import requests


class FineractApiClient:
    def __init__(
        self, api_base_url: str, tenant_id: str, api_username: str, api_password: str
    ):
        self.api_base_url = api_base_url
        self.tenant_id = tenant_id
        self.api_username = api_username
        self.api_password = api_password
        self.request_timeout_seconds = 30
        self.session = requests.Session()

        for endpoint_name, endpoint_class in endpoints.endpoint_classes():
            setattr(
                self,
                endpoint_name,
                endpoint_class(
                    self.session,
                    self.api_base_url,
                    self.request_timeout_seconds,
                ),
            )

    def authenticate(self):
        try:
            res = self.session.post(
                f"{self.api_base_url}/authentication",
                headers={
                    "Accept": "application/json",
                    "fineract-platform-tenantid": self.tenant_id,
                },
                json={
                    "username": self.api_username,
                    "password": self.api_password,
                },
                timeout=self.request_timeout_seconds,
            )
        except requests.RequestException:
            self.close()
            raise

        if not res.ok:
            self.close()
            raise Exception(
                f"Failed to authenticate with API: {res.status_code} - {res.text}"
            )

        try:
            res_json = res.json()
        except requests.JSONDecodeError:
            self.close()
            raise

        if "base64EncodedAuthenticationKey" not in res_json:
            self.close()
            raise Exception(
                "Failed to authenticate with API: Missing authentication key"
            )

        self.session.headers.update(
            {
                "Accept": "application/json",
                "fineract-platform-tenantid": self.tenant_id,
                "Authorization": f"Basic {res_json['base64EncodedAuthenticationKey']}",
            }
        )

    def close(self):
        self.session.close()
