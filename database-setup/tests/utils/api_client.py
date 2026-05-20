import requests

class FineractApiClient:
    def __init__(self, api_base_url: str, tenant_id:str, api_username:str, api_password:str):
        self.api_base_url = api_base_url
        self.tenant_id = tenant_id
        self.api_username = api_username
        self.api_password = api_password
        self.REQUEST_TIMEOUT_SECONDS = 30
        self.session = requests.Session()

    def get_authentication(self):
        try:
            res = self.session.post(
                f"{self.api_base_url}/authentication",
                headers={"fineract-platform-tenantid": self.tenant_id},
                json={
                    "username": self.api_username,
                    "password": self.api_password,
                },
                timeout=self.REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException as exc:
            self.session.close()
            raise Exception(f"Failed to connect to Fineract API: {exc}")

        if not res.ok:
            self.session.close()
            raise Exception(f"Failed to authenticate with API: {res.status_code} - {res.text}")

        try:
            res_json = res.json()
        except requests.JSONDecodeError as exc:
            self.session.close()
            raise Exception(f"Failed to parse authentication response as JSON: {exc}")

        if "base64EncodedAuthenticationKey" not in res_json:
            self.session.close()
            raise Exception("Failed to authenticate with API: Missing authentication key")

        self.session.headers.update(
            {
                "fineract-platform-tenantid": self.tenant_id,
                "Authorization": f"Basic {res_json['base64EncodedAuthenticationKey']}",
            }
        )
    
    def close(self):
        self.session.close()
    
