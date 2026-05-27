import pytest
from api.api_client import FineractApiClient
from api.endpoints.offices import OfficesEndpoint
from sqlalchemy.engine import Connection
from helpers.offices_helper import (
    assert_offices_present,
    create_missing_offices,
    load_offices,
)


@pytest.fixture(scope="module")
def offices_api(authenticated_api_client: FineractApiClient) -> OfficesEndpoint:
    return authenticated_api_client.offices # type: ignore


def test_offices_are_seeded(
    offices_api: OfficesEndpoint,
    db_connection: Connection
):
    offices = load_offices("offices.json")

    create_missing_offices(
        offices_api=offices_api,
        db_connection=db_connection,
        offices=offices,
    )

    assert_offices_present(
        db_connection=db_connection,
        offices=offices,
    )
