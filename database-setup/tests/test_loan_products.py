import pytest
from api.api_client import FineractApiClient
from api.endpoints.loan_products import LoanProductsEndpoint
from helpers.loan_products_helper import assert_loan_products_present, create_missing_loan_products, load_loan_products
from sqlalchemy.engine import Connection


@pytest.fixture(scope="module")
def loan_products_api(authenticated_api_client: FineractApiClient) -> LoanProductsEndpoint:
    """Return the authenticated loan products endpoint helper."""
    return authenticated_api_client.loan_products  # type: ignore


def test_loan_products_are_seeded(loan_products_api: LoanProductsEndpoint, db_connection: Connection):
    """Create missing loan products and verify their database fields."""
    loan_products = load_loan_products("loan_products.json")

    create_missing_loan_products(
        loan_products_api=loan_products_api,
        db_connection=db_connection,
        loan_products=loan_products,
    )

    assert_loan_products_present(
        db_connection=db_connection,
        loan_products=loan_products,
    )
