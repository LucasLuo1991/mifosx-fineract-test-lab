from pathlib import Path

from api.endpoints.staff import StaffEndpoint, StaffPayload
from helpers.seed_helper import (
    assert_items_present,
    create_missing_items,
    load_seed_data,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection

STAFF_DATA_DIR = Path(__file__).parents[1] / "data"

STAFF_DISPLAY_NAMES_QUERY = text("""
    SELECT s.display_name
    FROM m_staff s
""")


def load_staff(file_name: str) -> list[StaffPayload]:
    return load_seed_data(STAFF_DATA_DIR, file_name)


def get_staff_names(db_connection: Connection) -> set[str]:
    result = db_connection.execute(STAFF_DISPLAY_NAMES_QUERY)
    return set(result.scalars())


def create_missing_staff(
    staff_api: StaffEndpoint,
    db_connection: Connection,
    staff_members: list[StaffPayload],
) -> None:
    existing_staff = get_staff_names(db_connection)

    create_missing_items(
        items=staff_members,
        existing_names=existing_staff,
        create_item=staff_api.create_staff,
        name_key="display_name",
    )


def assert_staff_present(
    db_connection: Connection,
    staff: list[StaffPayload],
) -> None:
    expected_names = {employee["display_name"] for employee in staff}
    actual_names = get_staff_names(db_connection)

    assert_items_present(
        expected_names=expected_names,
        actual_names=actual_names,
        label="staff",
    )
