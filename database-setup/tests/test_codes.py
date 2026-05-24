import pytest
from api.api_client import FineractApiClient
from api.endpoints.codes import CodesEndpoint
from sqlalchemy.engine import Connection
from helpers.codes.code_values import (
    assert_code_values_present,
    create_missing_code_values,
    load_code_values,
)


@pytest.fixture(scope="module")
def codes_api(authenticated_api_client: FineractApiClient):
    return authenticated_api_client.codes


@pytest.mark.parametrize(
    ("tested_code_name", "code_values_file_name"),
    [
        ("Gender", "gender_code_values.json"),
    ],
)
def test_code_values_are_seeded(
    codes_api: CodesEndpoint,
    db_connection: Connection,
    tested_code_name: str,
    code_values_file_name: str,
):
    code_values = load_code_values(code_values_file_name)

    assert (
        codes_api.get_code_by_name(tested_code_name).get("name") == tested_code_name
    ), f"Expected to find a code named '{tested_code_name}'"

    create_missing_code_values(
        codes_api=codes_api,
        db_connection=db_connection,
        code_name=tested_code_name,
        code_values=code_values,
    )

    assert_code_values_present(
        db_connection=db_connection,
        code_name=tested_code_name,
        expected_code_values=code_values,
    )
