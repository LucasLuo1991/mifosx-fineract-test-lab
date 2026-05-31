from pathlib import Path
from typing import cast

from api.endpoints.loan_products import LoanProductPayload, LoanProductsEndpoint
from helpers.seed_helper import (
    SeedFieldMapping,
    assert_seed_items_match_db,
    create_missing_items,
    load_seed_data,
    normalize_decimal,
    normalize_optional_zero_decimal,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection

LOAN_PRODUCTS_DATA_DIR = Path(__file__).parents[1] / "data"

LOAN_PRODUCTS_ROWS_QUERY = text("""
    SELECT
        pl.name,
        pl.short_name,
        pl.description,
        pl.currency_code,
        pl.currency_digits,
        pl.currency_multiplesof,
        pl.principal_amount,
        pl.number_of_repayments,
        pl.repay_every,
        pl.repayment_period_frequency_enum,
        pl.nominal_interest_rate_per_period,
        pl.interest_period_frequency_enum,
        pl.amortization_method_enum,
        pl.interest_method_enum,
        pl.interest_calculated_in_period_enum,
        pl.accounting_type,
        pl.interest_recalculation_enabled,
        pl.days_in_year_enum,
        pl.days_in_month_enum,
        pl.arrearstolerance_amount,
        pl.include_in_borrower_cycle,
        pl.use_borrower_cycle,
        pl.can_define_fixed_emi_amount,
        pl.allow_variabe_installments,
        pl.allow_partial_period_interest_calcualtion,
        pl.enable_down_payment,
        pl.enable_buy_down_fee,
        pl.hold_guarantee_funds,
        pl.account_moves_out_of_npa_only_on_arrears_completion
    FROM m_product_loan pl;
""")

LOAN_PRODUCTS_NAMES_QUERY = text("""
    SELECT pl.name
    FROM m_product_loan pl;
""")

LOAN_PRODUCTS_FIELD_MAPPINGS = (
    SeedFieldMapping("name", "name"),
    SeedFieldMapping("shortName", "short_name"),
    SeedFieldMapping("description", "description"),
    SeedFieldMapping("currencyCode", "currency_code"),
    SeedFieldMapping("digitsAfterDecimal", "currency_digits"),
    SeedFieldMapping("inMultiplesOf", "currency_multiplesof"),
    SeedFieldMapping("principal", "principal_amount", normalize_decimal),
    SeedFieldMapping("numberOfRepayments", "number_of_repayments"),
    SeedFieldMapping("repaymentEvery", "repay_every"),
    SeedFieldMapping("repaymentFrequencyType", "repayment_period_frequency_enum"),
    SeedFieldMapping("interestRatePerPeriod", "nominal_interest_rate_per_period", normalize_decimal),
    SeedFieldMapping("interestRateFrequencyType", "interest_period_frequency_enum"),
    SeedFieldMapping("amortizationType", "amortization_method_enum"),
    SeedFieldMapping("interestType", "interest_method_enum"),
    SeedFieldMapping("interestCalculationPeriodType", "interest_calculated_in_period_enum"),
    SeedFieldMapping("accountingRule", "accounting_type"),
    SeedFieldMapping("isInterestRecalculationEnabled", "interest_recalculation_enabled"),
    SeedFieldMapping("daysInYearType", "days_in_year_enum"),
    SeedFieldMapping("daysInMonthType", "days_in_month_enum"),
    SeedFieldMapping(
        "inArrearsTolerance",
        "arrearstolerance_amount",
        normalize_optional_zero_decimal,
    ),
    SeedFieldMapping("includeInBorrowerCycle", "include_in_borrower_cycle"),
    SeedFieldMapping("useBorrowerCycle", "use_borrower_cycle"),
    SeedFieldMapping("canDefineInstallmentAmount", "can_define_fixed_emi_amount"),
    SeedFieldMapping("allowVariableInstallments", "allow_variabe_installments"),
    SeedFieldMapping("allowPartialPeriodInterestCalculation", "allow_partial_period_interest_calcualtion"),
    SeedFieldMapping("enableDownPayment", "enable_down_payment"),
    SeedFieldMapping("enableBuyDownFee", "enable_buy_down_fee"),
    SeedFieldMapping("holdGuaranteeFunds", "hold_guarantee_funds"),
    SeedFieldMapping(
        "accountMovesOutOfNPAOnlyOnArrearsCompletion",
        "account_moves_out_of_npa_only_on_arrears_completion",
    ),
)


def load_loan_products(file_name: str) -> list[LoanProductPayload]:
    return cast(
        list[LoanProductPayload],
        load_seed_data(LOAN_PRODUCTS_DATA_DIR, file_name),
    )


def get_loan_products_names(db_connection: Connection) -> set[str]:
    result = db_connection.execute(LOAN_PRODUCTS_NAMES_QUERY)
    return set(result.scalars())


def get_loan_products_rows(db_connection: Connection):
    result = db_connection.execute(LOAN_PRODUCTS_ROWS_QUERY)
    return result.mappings().all()


def create_missing_loan_products(
    loan_products_api: LoanProductsEndpoint,
    db_connection: Connection,
    loan_products: list[LoanProductPayload],
) -> None:
    existing_loan_products = get_loan_products_names(db_connection)

    create_missing_items(
        items=loan_products,
        existing_names=existing_loan_products,
        create_item=loan_products_api.create_loan_product,
    )


def assert_loan_products_present(
    db_connection: Connection,
    loan_products: list[LoanProductPayload],
) -> None:
    assert_seed_items_match_db(
        expected_items=loan_products,
        actual_rows=get_loan_products_rows(db_connection),
        label="loan products",
        field_mappings=LOAN_PRODUCTS_FIELD_MAPPINGS,
    )
