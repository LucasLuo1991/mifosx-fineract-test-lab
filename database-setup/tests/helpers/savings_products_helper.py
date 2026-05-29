from pathlib import Path

from api.endpoints.savings_products import (
    SavingsProductPayload,
    SavingsProductsEndpoint,
)
from helpers.seed_helper import (
    assert_items_present,
    create_missing_items,
    load_seed_data,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection

SAVINGS_PRODUCTS_DATA_DIR = Path(__file__).parents[1] / "data"

SAVINGS_PRODUCTS_NAMES_QUERY = text("""
    SELECT sp.name
    FROM m_savings_product sp;
""")


def load_savings_products(file_name: str) -> list[SavingsProductPayload]:
    return load_seed_data(SAVINGS_PRODUCTS_DATA_DIR, file_name)


def get_savings_products_names(db_connection: Connection) -> set[str]:
    result = db_connection.execute(SAVINGS_PRODUCTS_NAMES_QUERY)
    return set(result.scalars())


def create_missing_savings_products(
    savings_products_api: SavingsProductsEndpoint,
    db_connection: Connection,
    savings_products: list[SavingsProductPayload],
) -> None:
    existing_savings_products = get_savings_products_names(db_connection)

    create_missing_items(
        items=savings_products,
        existing_names=existing_savings_products,
        create_item=savings_products_api.create_savings_product,
    )


def assert_savings_products_present(
    db_connection: Connection,
    savings_products: list[SavingsProductPayload],
) -> None:
    expected_names = {savings_product["name"] for savings_product in savings_products}
    actual_names = get_savings_products_names(db_connection)

    assert_items_present(
        expected_names=expected_names,
        actual_names=actual_names,
        label="savings products",
    )
