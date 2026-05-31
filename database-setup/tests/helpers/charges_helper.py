from pathlib import Path

from api.endpoints.charges import ChargePayload, ChargesEndpoint
from helpers.seed_helper import (
    assert_items_present,
    create_missing_items,
    load_seed_data,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection

CHARGES_DATA_DIR = Path(__file__).parents[1] / "data"

CHARGES_NAMES_QUERY = text("""
    SELECT c.name
    FROM m_charge c
""")


def load_charges(file_name: str) -> list[ChargePayload]:
    return load_seed_data(CHARGES_DATA_DIR, file_name)


def get_charges_names(db_connection: Connection) -> set[str]:
    result = db_connection.execute(CHARGES_NAMES_QUERY)
    return set(result.scalars())


def create_missing_charges(
    charges_api: ChargesEndpoint,
    db_connection: Connection,
    charges: list[ChargePayload],
) -> None:
    existing_charges = get_charges_names(db_connection)

    create_missing_items(
        items=charges,
        existing_names=existing_charges,
        create_item=charges_api.create_charge,
    )


def assert_charges_present(
    db_connection: Connection,
    charges: list[ChargePayload],
) -> None:
    expected_names = {charge["name"] for charge in charges}
    actual_names = get_charges_names(db_connection)

    assert_items_present(
        expected_names=expected_names,
        actual_names=actual_names,
        label="charges",
    )
