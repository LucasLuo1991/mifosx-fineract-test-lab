import pytest
from api.api_client import FineractApiClient
from api.endpoints.charges import ChargesEndpoint
from helpers.charges_helper import (
    assert_charges_present,
    create_missing_charges,
    load_charges,
)
from sqlalchemy.engine import Connection


@pytest.fixture(scope="module")
def charges_api(authenticated_api_client: FineractApiClient) -> ChargesEndpoint:
    return authenticated_api_client.charges  # type: ignore


def test_charges_are_seeded(charges_api: ChargesEndpoint, db_connection: Connection):
    charges = load_charges("charges.json")

    create_missing_charges(
        charges_api=charges_api,
        db_connection=db_connection,
        charges=charges,
    )

    assert_charges_present(
        db_connection=db_connection,
        charges=charges,
    )
