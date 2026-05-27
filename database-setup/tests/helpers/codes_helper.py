from pathlib import Path

from api.endpoints.codes import CodesEndpoint, CodeValuePayload
from helpers.seed_helper import (
    assert_items_present,
    create_missing_items,
    load_seed_data,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection

CODE_VALUES_DATA_DIR = Path(__file__).parents[1] / "data" / "codes"

CODE_VALUE_NAMES_BY_CODE_NAME_QUERY = text("""
    SELECT
        v.code_value
    FROM m_code c
    JOIN m_code_value v ON c.id = v.code_id
    WHERE c.code_name = :code_name;
""")


def load_code_values(file_name: str) -> list[CodeValuePayload]:
    return load_seed_data(CODE_VALUES_DATA_DIR, file_name)


def get_code_value_names(db_connection: Connection, code_name: str) -> set[str]:
    result = db_connection.execute(
        CODE_VALUE_NAMES_BY_CODE_NAME_QUERY,
        {"code_name": code_name},
    )
    return set(result.scalars())


def create_missing_code_values(
    codes_api: CodesEndpoint,
    db_connection: Connection,
    code_name: str,
    code_values: list[CodeValuePayload],
) -> None:
    existing_code_values = get_code_value_names(db_connection, code_name)

    create_missing_items(
        items=code_values,
        existing_names=existing_code_values,
        create_item=lambda code_value: codes_api.create_code_values_by_name(
            code_name=code_name,
            code_value=code_value,
        ),
    )


def assert_code_values_present(
    db_connection: Connection,
    code_name: str,
    expected_code_values: list[CodeValuePayload],
) -> None:
    expected_names = {code_value["name"] for code_value in expected_code_values}
    actual_names = get_code_value_names(db_connection, code_name)

    assert_items_present(
        expected_names=expected_names,
        actual_names=actual_names,
        label=f"code values for '{code_name}'",
    )
