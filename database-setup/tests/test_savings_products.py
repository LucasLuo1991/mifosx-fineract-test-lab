import pytest
from api.api_client import FineractApiClient
from api.endpoints.savings_products import SavingsProductsEndpoint
from helpers.savings_products_helper import (
    assert_savings_products_present,
    create_missing_savings_products,
    load_savings_products,
)
from sqlalchemy.engine import Connection


@pytest.fixture(scope="module")
def savings_products_api(
    authenticated_api_client: FineractApiClient,
) -> SavingsProductsEndpoint:
    """Return the authenticated savings products endpoint helper."""
    return authenticated_api_client.savings_products  # type: ignore


def test_savings_products_are_seeded(
    savings_products_api: SavingsProductsEndpoint, db_connection: Connection
):
    """Create missing savings products and verify their database fields."""
    savings_products = load_savings_products("savings_products.json")

    create_missing_savings_products(
        savings_products_api=savings_products_api,
        db_connection=db_connection,
        savings_products=savings_products,
    )

    assert_savings_products_present(
        db_connection=db_connection,
        savings_products=savings_products,
    )
