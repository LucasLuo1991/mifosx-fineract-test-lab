import pytest
from api.api_client import FineractApiClient
from api.endpoints.codes import CodesEndpoint


@pytest.fixture(scope="module")
def codes_api(authenticated_api_client: FineractApiClient):
    return authenticated_api_client.codes


def test_all_codes_present(codes_api: CodesEndpoint):
    codes = codes_api.get_all_codes()
    assert isinstance(codes, dict), "Expected a list of codes"
