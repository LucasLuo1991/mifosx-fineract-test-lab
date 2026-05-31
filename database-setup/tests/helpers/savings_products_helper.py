from pathlib import Path
from typing import cast

from api.endpoints.savings_products import (
    SavingsProductPayload,
    SavingsProductsEndpoint,
)
from helpers.seed_helper import (
    SeedFieldMapping,
    assert_seed_items_match_db,
    create_missing_items,
    load_seed_data,
    normalize_decimal,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection

SAVINGS_PRODUCTS_DATA_DIR = Path(__file__).parents[1] / "data"

SAVINGS_PRODUCTS_ROWS_QUERY = text("""
    SELECT
        sp.name,
        sp.short_name,
        sp.description,
        sp.currency_code,
        sp.currency_digits,
        sp.currency_multiplesof,
        sp.nominal_annual_interest_rate,
        sp.interest_compounding_period_enum,
        sp.interest_posting_period_enum,
        sp.interest_calculation_type_enum,
        sp.interest_calculation_days_in_year_type_enum,
        sp.accounting_type,
        sp.min_required_opening_balance,
        sp.lockin_period_frequency,
        sp.lockin_period_frequency_enum,
        sp.enforce_min_required_balance,
        sp.withdrawal_fee_for_transfer,
        sp.allow_overdraft,
        sp.withhold_tax,
        sp.is_dormancy_tracking_active,
        sp.is_lien_allowed
    FROM m_savings_product sp;
""")

SAVINGS_PRODUCTS_NAMES_QUERY = text("""
    SELECT sp.name
    FROM m_savings_product sp;
""")

SAVINGS_PRODUCTS_FIELD_MAPPINGS = (
    SeedFieldMapping("name", "name"),
    SeedFieldMapping("shortName", "short_name"),
    SeedFieldMapping("description", "description"),
    SeedFieldMapping("currencyCode", "currency_code"),
    SeedFieldMapping("digitsAfterDecimal", "currency_digits"),
    SeedFieldMapping("inMultiplesOf", "currency_multiplesof"),
    SeedFieldMapping("nominalAnnualInterestRate", "nominal_annual_interest_rate", normalize_decimal),
    SeedFieldMapping("interestCompoundingPeriodType", "interest_compounding_period_enum"),
    SeedFieldMapping("interestPostingPeriodType", "interest_posting_period_enum"),
    SeedFieldMapping("interestCalculationType", "interest_calculation_type_enum"),
    SeedFieldMapping("interestCalculationDaysInYearType", "interest_calculation_days_in_year_type_enum"),
    SeedFieldMapping("accountingRule", "accounting_type"),
    SeedFieldMapping("minRequiredOpeningBalance", "min_required_opening_balance", normalize_decimal),
    SeedFieldMapping("lockinPeriodFrequency", "lockin_period_frequency", normalize_decimal),
    SeedFieldMapping("lockinPeriodFrequencyType", "lockin_period_frequency_enum"),
    SeedFieldMapping("enforceMinRequiredBalance", "enforce_min_required_balance"),
    SeedFieldMapping("withdrawalFeeForTransfers", "withdrawal_fee_for_transfer"),
    SeedFieldMapping("allowOverdraft", "allow_overdraft"),
    SeedFieldMapping("withHoldTax", "withhold_tax"),
    SeedFieldMapping("isDormancyTrackingActive", "is_dormancy_tracking_active"),
    SeedFieldMapping("lienAllowed", "is_lien_allowed"),
)


def load_savings_products(file_name: str) -> list[SavingsProductPayload]:
    """Load savings product seed payloads from the shared test data directory."""
    return cast(
        list[SavingsProductPayload],
        load_seed_data(SAVINGS_PRODUCTS_DATA_DIR, file_name),
    )


def get_savings_products_names(db_connection: Connection) -> set[str]:
    """Return the names of savings products currently stored in Fineract."""
    result = db_connection.execute(SAVINGS_PRODUCTS_NAMES_QUERY)
    return set(result.scalars())


def get_savings_products_rows(db_connection: Connection):
    """Return savings product rows needed for seed verification."""
    result = db_connection.execute(SAVINGS_PRODUCTS_ROWS_QUERY)
    return result.mappings().all()


def create_missing_savings_products(
    savings_products_api: SavingsProductsEndpoint,
    db_connection: Connection,
    savings_products: list[SavingsProductPayload],
) -> None:
    """Create savings products that are not already present by name."""
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
    """Assert that savings product seed payloads match database rows."""
    assert_seed_items_match_db(
        expected_items=savings_products,
        actual_rows=get_savings_products_rows(db_connection),
        label="savings products",
        field_mappings=SAVINGS_PRODUCTS_FIELD_MAPPINGS,
    )
