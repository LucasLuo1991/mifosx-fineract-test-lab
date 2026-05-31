from pathlib import Path
from typing import cast

from api.endpoints.charges import ChargePayload, ChargesEndpoint
from helpers.seed_helper import (
    SeedFieldMapping,
    assert_seed_items_match_db,
    create_missing_items,
    load_seed_data,
    normalize_decimal,
    normalize_fee_month_day_day,
    normalize_fee_month_day_month,
    normalize_optional_int,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection

CHARGES_DATA_DIR = Path(__file__).parents[1] / "data"

CHARGES_ROWS_QUERY = text("""
    SELECT
        c.name,
        c.currency_code,
        c.amount,
        c.charge_applies_to_enum,
        c.charge_time_enum,
        c.charge_calculation_enum,
        c.charge_payment_mode_enum,
        c.is_active,
        c.is_penalty,
        c.fee_frequency,
        c.fee_interval,
        c.fee_on_day,
        c.fee_on_month,
        c.min_cap,
        c.max_cap
    FROM m_charge c;
""")

CHARGES_NAMES_QUERY = text("""
    SELECT c.name
    FROM m_charge c;
""")

CHARGES_FIELD_MAPPINGS = (
    SeedFieldMapping("name", "name"),
    SeedFieldMapping("currencyCode", "currency_code"),
    SeedFieldMapping("amount", "amount", normalize_decimal),
    SeedFieldMapping("chargeAppliesTo", "charge_applies_to_enum"),
    SeedFieldMapping("chargeTimeType", "charge_time_enum"),
    SeedFieldMapping("chargeCalculationType", "charge_calculation_enum"),
    SeedFieldMapping("chargePaymentMode", "charge_payment_mode_enum"),
    SeedFieldMapping("active", "is_active"),
    SeedFieldMapping("penalty", "is_penalty"),
    SeedFieldMapping("feeFrequency", "fee_frequency"),
    SeedFieldMapping("feeInterval", "fee_interval", normalize_optional_int),
    SeedFieldMapping("feeOnMonthDay", "fee_on_day", normalize_fee_month_day_day),
    SeedFieldMapping("feeOnMonthDay", "fee_on_month", normalize_fee_month_day_month),
    SeedFieldMapping("minCap", "min_cap", normalize_decimal),
    SeedFieldMapping("maxCap", "max_cap", normalize_decimal),
)


def load_charges(file_name: str) -> list[ChargePayload]:
    return cast(list[ChargePayload], load_seed_data(CHARGES_DATA_DIR, file_name))


def get_charges_names(db_connection: Connection) -> set[str]:
    result = db_connection.execute(CHARGES_NAMES_QUERY)
    return set(result.scalars())


def get_charges_rows(db_connection: Connection):
    result = db_connection.execute(CHARGES_ROWS_QUERY)
    return result.mappings().all()


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
    assert_seed_items_match_db(
        expected_items=charges,
        actual_rows=get_charges_rows(db_connection),
        label="charges",
        field_mappings=CHARGES_FIELD_MAPPINGS,
    )
