from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

from api.endpoints.codes import CodesEndpoint, CodeValuePayload
from helpers.seed_helper import (
    SeedFieldMapping,
    assert_seed_items_match_db,
    create_missing_items,
    load_seed_data,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection, RowMapping

CODE_VALUES_DATA_DIR = Path(__file__).parents[1] / "data" / "codes"

CODE_VALUE_ROWS_BY_CODE_NAME_QUERY = text("""
    SELECT
        v.code_value,
        v.id,
        v.code_description,
        v.order_position,
        v.is_active
    FROM m_code c
    JOIN m_code_value v ON c.id = v.code_id
    WHERE c.code_name = :code_name;
""")

CODE_VALUE_FIELD_MAPPINGS = (
    SeedFieldMapping("name", "code_value"),
    SeedFieldMapping("description", "code_description"),
    SeedFieldMapping("position", "order_position"),
    SeedFieldMapping("isActive", "is_active"),
)


def load_code_values(file_name: str) -> list[CodeValuePayload]:
    return cast(list[CodeValuePayload], load_seed_data(CODE_VALUES_DATA_DIR, file_name))


def get_code_value_names(db_connection: Connection, code_name: str) -> set[str]:
    result = db_connection.execute(
        CODE_VALUE_ROWS_BY_CODE_NAME_QUERY,
        {"code_name": code_name},
    )
    return set(result.scalars())


def get_code_value_rows(db_connection: Connection, code_name: str):
    result = db_connection.execute(
        CODE_VALUE_ROWS_BY_CODE_NAME_QUERY,
        {"code_name": code_name},
    )
    return result.mappings().all()


def create_missing_code_values(
    codes_api: CodesEndpoint,
    db_connection: Connection,
    code_name: str,
    code_values: list[CodeValuePayload],
) -> None:
    existing_rows = get_code_value_rows(db_connection, code_name)
    existing_code_values = {row["code_value"] for row in existing_rows}

    create_missing_items(
        items=code_values,
        existing_names=existing_code_values,
        create_item=lambda code_value: codes_api.create_code_values_by_name(
            code_name=code_name,
            code_value=code_value,
        ),
    )

    rows_by_name = {row["code_value"]: row for row in existing_rows}
    for code_value in code_values:
        existing_row = rows_by_name.get(code_value["name"])

        if existing_row is not None and _code_value_needs_update(
            code_value,
            existing_row,
        ):
            codes_api.update_code_values_by_name(
                code_name=code_name,
                code_value_id=existing_row["id"],
                code_value=code_value,
            )


def assert_code_values_present(
    db_connection: Connection,
    code_name: str,
    expected_code_values: list[CodeValuePayload],
) -> None:
    assert_seed_items_match_db(
        expected_items=expected_code_values,
        actual_rows=get_code_value_rows(db_connection, code_name),
        label=f"code values for '{code_name}'",
        identity_json_key="name",
        identity_db_column="code_value",
        field_mappings=CODE_VALUE_FIELD_MAPPINGS,
    )


def _code_value_needs_update(
    expected_code_value: CodeValuePayload,
    actual_row: RowMapping,
) -> bool:
    expected_values = cast(Mapping[str, Any], expected_code_value)

    return any(
        actual_row[field_mapping.db_column] != expected_values[field_mapping.json_key]
        for field_mapping in CODE_VALUE_FIELD_MAPPINGS
    )
