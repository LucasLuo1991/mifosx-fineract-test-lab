from pathlib import Path
from typing import cast

from api.endpoints.offices import OfficePayload, OfficesEndpoint
from helpers.seed_helper import (
    SeedFieldMapping,
    assert_seed_items_match_db,
    create_missing_items,
    load_seed_data,
    normalize_seed_date,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection

OFFICES_DATA_DIR = Path(__file__).parents[1] / "data"

OFFICE_ROWS_QUERY = text("""
    SELECT
        o.name,
        o.external_id,
        o.parent_id,
        o.opening_date
    FROM m_office o
    ORDER BY id;
""")

OFFICE_NAMES_QUERY = text("""
    SELECT o.name
    FROM m_office o;
""")

OFFICE_FIELD_MAPPINGS = (
    SeedFieldMapping("name", "name"),
    SeedFieldMapping("externalId", "external_id"),
    SeedFieldMapping("parentId", "parent_id"),
    SeedFieldMapping("openingDate", "opening_date", normalize_seed_date),
)


def load_offices(file_name: str) -> list[OfficePayload]:
    """Load office seed payloads from the shared test data directory."""
    return cast(list[OfficePayload], load_seed_data(OFFICES_DATA_DIR, file_name))


def get_office_names(db_connection: Connection) -> set[str]:
    """Return the names of offices currently stored in Fineract."""
    result = db_connection.execute(OFFICE_NAMES_QUERY)
    return set(result.scalars())


def get_office_rows(db_connection: Connection):
    """Return office rows needed for seed verification."""
    result = db_connection.execute(OFFICE_ROWS_QUERY)
    return result.mappings().all()


def create_missing_offices(
    offices_api: OfficesEndpoint,
    db_connection: Connection,
    offices: list[OfficePayload],
) -> None:
    """Create office records that are not already present by name."""
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
    """Assert that office seed payloads are present with matching DB fields."""
    assert_seed_items_match_db(
        expected_items=offices,
        actual_rows=get_office_rows(db_connection),
        label="offices",
        field_mappings=OFFICE_FIELD_MAPPINGS,
    )
