from pathlib import Path

from api.endpoints.offices import OfficePayload, OfficesEndpoint
from helpers.seed_helper import (
    assert_items_present,
    create_missing_items,
    load_seed_data,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection

OFFICES_DATA_DIR = Path(__file__).parents[1] / "data"

OFFICE_NAMES_QUERY = text("""
    SELECT o.name
    FROM m_office o
    ORDER BY id
""")


def load_offices(file_name: str) -> list[OfficePayload]:
    return load_seed_data(OFFICES_DATA_DIR, file_name)


def get_office_names(db_connection: Connection) -> set[str]:
    result = db_connection.execute(OFFICE_NAMES_QUERY)
    return set(result.scalars())


def create_missing_offices(
    offices_api: OfficesEndpoint,
    db_connection: Connection,
    offices: list[OfficePayload],
) -> None:
    existing_offices = get_office_names(db_connection)

    create_missing_items(
        items=offices,
        existing_names=existing_offices,
        create_item=offices_api.create_office,
    )


def assert_offices_present(
    db_connection: Connection,
    offices: list[OfficePayload],
) -> None:
    expected_names = {office["name"] for office in offices}
    actual_names = get_office_names(db_connection)

    assert_items_present(
        expected_names=expected_names,
        actual_names=actual_names,
        label="offices",
    )
