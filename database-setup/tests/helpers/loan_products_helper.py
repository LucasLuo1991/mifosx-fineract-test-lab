from pathlib import Path

from api.endpoints.loan_products import LoanProductPayload, LoanProductsEndpoint
from helpers.seed_helper import (
    assert_items_present,
    create_missing_items,
    load_seed_data,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection

LOAN_PRODUCTS_DATA_DIR = Path(__file__).parents[1] / "data"

LOAN_PRODUCTS_NAMES_QUERY = text("""
    SELECT pl.name
    FROM m_product_loan pl;
""")


def load_loan_products(file_name: str) -> list[LoanProductPayload]:
    return load_seed_data(LOAN_PRODUCTS_DATA_DIR, file_name)


def get_loan_products_names(db_connection: Connection) -> set[str]:
    result = db_connection.execute(LOAN_PRODUCTS_NAMES_QUERY)
    return set(result.scalars())


def create_missing_loan_products(
    loan_products_api: LoanProductsEndpoint,
    db_connection: Connection,
    loan_products: list[LoanProductPayload],
) -> None:
    existing_loan_products = get_loan_products_names(db_connection)

    create_missing_items(
        items=loan_products,
        existing_names=existing_loan_products,
        create_item=loan_products_api.create_loan_product,
    )


def assert_loan_products_present(
    db_connection: Connection,
    loan_products: list[LoanProductPayload],
) -> None:
    expected_names = {loan_product["name"] for loan_product in loan_products}
    actual_names = get_loan_products_names(db_connection)

    assert_items_present(
        expected_names=expected_names,
        actual_names=actual_names,
        label="loan products",
    )
