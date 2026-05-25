from pathlib import Path
from typing import Any

from api.endpoints.codes import CodesEndpoint
from sqlalchemy import text
from sqlalchemy.engine import Connection
from utils.json_loader import load_json

CODE_VALUES_DATA_DIR = Path(__file__).parents[1] / "data" / "codes"

CODE_VALUE_NAMES_BY_CODE_NAME_QUERY = text("""
    SELECT
        v.code_value
    FROM m_code c
    JOIN m_code_value v ON c.id = v.code_id
    WHERE c.code_name = :code_name;
""")


def load_code_values(file_name: str) -> list[dict[str, Any]]:
    return load_json(CODE_VALUES_DATA_DIR / file_name)


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
    code_values: list[dict[str, Any]],
) -> None:
    existing_code_values = get_code_value_names(db_connection, code_name)

    for code_value in code_values:
        if code_value["name"] not in existing_code_values:
            codes_api.create_code_values_by_name(
                code_name=code_name,
                code_value=code_value,
            )
            existing_code_values.add(code_value["name"])


def assert_code_values_present(
    db_connection: Connection,
    code_name: str,
    expected_code_values: list[dict[str, Any]],
) -> None:
    expected_names = {code_value["name"] for code_value in expected_code_values}
    actual_names = get_code_value_names(db_connection, code_name)
    missing_names = expected_names - actual_names

    assert not missing_names, (
        f"Missing code values for '{code_name}': {sorted(missing_names)}. "
        f"Actual values: {sorted(actual_names)}"
    )
