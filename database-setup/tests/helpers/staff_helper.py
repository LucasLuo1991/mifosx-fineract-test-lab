from pathlib import Path
from typing import cast

from api.endpoints.staff import StaffEndpoint, StaffPayload
from helpers.seed_helper import (
    SeedFieldMapping,
    assert_seed_items_match_db,
    create_missing_items,
    load_seed_data,
    normalize_seed_date,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection

STAFF_DATA_DIR = Path(__file__).parents[1] / "data"

STAFF_ROWS_QUERY = text("""
    SELECT
        s.display_name,
        s.firstname,
        s.lastname,
        s.mobile_no,
        s.external_id,
        s.email_address,
        s.office_id,
        s.is_active,
        s.is_loan_officer,
        s.joining_date
    FROM m_staff s;
""")

STAFF_NAMES_QUERY = text("""
    SELECT s.display_name
    FROM m_staff s;
""")

STAFF_FIELD_MAPPINGS = (
    SeedFieldMapping("display_name", "display_name"),
    SeedFieldMapping("firstname", "firstname"),
    SeedFieldMapping("lastname", "lastname"),
    SeedFieldMapping("mobileNo", "mobile_no"),
    SeedFieldMapping("externalId", "external_id"),
    SeedFieldMapping("emailAddress", "email_address"),
    SeedFieldMapping("officeId", "office_id"),
    SeedFieldMapping("isActive", "is_active"),
    SeedFieldMapping("isLoanOfficer", "is_loan_officer"),
    SeedFieldMapping("joiningDate", "joining_date", normalize_seed_date),
)


def load_staff(file_name: str) -> list[StaffPayload]:
    return cast(list[StaffPayload], load_seed_data(STAFF_DATA_DIR, file_name))


def get_staff_names(db_connection: Connection) -> set[str]:
    result = db_connection.execute(STAFF_NAMES_QUERY)
    return set(result.scalars())


def get_staff_rows(db_connection: Connection):
    result = db_connection.execute(STAFF_ROWS_QUERY)
    return result.mappings().all()


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
    assert_seed_items_match_db(
        expected_items=staff,
        actual_rows=get_staff_rows(db_connection),
        label="staff",
        identity_json_key="display_name",
        field_mappings=STAFF_FIELD_MAPPINGS,
    )
