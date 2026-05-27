import pytest
from api.api_client import FineractApiClient
from api.endpoints.codes import CodesEndpoint
from sqlalchemy.engine import Connection
from helpers.code_values import (
    assert_code_values_present,
    create_missing_code_values,
    load_code_values,
)


@pytest.fixture(scope="module")
def codes_api(authenticated_api_client: FineractApiClient) -> CodesEndpoint:
    return authenticated_api_client.codes # type: ignore


@pytest.mark.parametrize(
    ("tested_code_name", "code_values_file_name"),
    [
        ("ADDRESS_TYPE", "address_type.json"),
        ("AssetAccountTags", "asset_account_tags.json"),
        (
            "buydown_fee_transaction_classification",
            "buydown_fee_transaction_classification.json",
        ),
        (
            "capitalized_income_transaction_classification",
            "capitalized_income_transaction_classification.json",
        ),
        ("CenterClosureReason", "center_closure_reason.json"),
        ("ChargeOffReasons", "charge_off_reasons.json"),
        ("ClientClassification", "client_classification.json"),
        ("ClientClosureReason", "client_closure_reason.json"),
        ("ClientRejectReason", "client_reject_reason.json"),
        ("ClientSubStatus", "client_sub_status.json"),
        ("ClientType", "client_type.json"),
        ("ClientWithdrawReason", "client_withdraw_reason.json"),
        ("Constitution", "constitution.json"),
        ("COUNTRY", "country.json"),
        ("CreditTransactionFreezeReasons", "credit_transaction_freeze_reasons.json"),
        ("Customer Documents", "customer_documents.json"),
        ("Customer Identifier", "customer_identifier.json"),
        ("DebitTransactionFreezeReasons", "debit_transaction_freeze_reasons.json"),
        ("Entity to Entity Access Types", "entity_to_entity_access_types.json"),
        ("EquityAccountTags", "equity_account_tags.json"),
        ("ExpenseAccountTags", "expense_account_tags.json"),
        ("Gender", "gender.json"),
        ("GroupClosureReason", "group_closure_reason.json"),
        ("GROUPROLE", "group_role.json"),
        ("GuarantorRelationship", "guarantor_relationship.json"),
        ("IncomeAccountTags", "income_account_tags.json"),
        ("LiabilityAccountTags", "liability_account_tags.json"),
        ("LoanCollateral", "loan_collateral.json"),
        ("LoanOriginationChannelType", "loan_origination_channel_type.json"),
        ("LoanOriginatorType", "loan_originator_type.json"),
        ("LoanPurpose", "loan_purpose.json"),
        ("LoanRescheduleReason", "loan_reschedule_reason.json"),
        ("Main Business Line", "main_business_line.json"),
        ("MARITAL STATUS", "marital_status.json"),
        ("PaymentType", "payment_type.json"),
        ("PROFESSION", "profession.json"),
        ("ReAgeReasons", "re_age_reasons.json"),
        ("ReAmortizationReasons", "re_amortization_reasons.json"),
        ("RELATIONSHIP", "relationship.json"),
        ("SavingsAccountBlockReasons", "savings_account_block_reasons.json"),
        (
            "SavingsTransactionFreezeReasons",
            "savings_transaction_freeze_reasons.json",
        ),
        ("STATE", "state.json"),
        (
            "working_capital_loan_credit_balance_refund_classification",
            "working_capital_loan_credit_balance_refund_classification.json",
        ),
        (
            "working_capital_loan_disbursement_classification",
            "working_capital_loan_disbursement_classification.json",
        ),
        (
            "working_capital_loan_repayment_classification",
            "working_capital_loan_repayment_classification.json",
        ),
        ("WriteOffReasons", "write_off_reasons.json"),
        ("YesNo", "yes_no.json"),
    ],
)
def test_code_values_are_seeded(
    codes_api: CodesEndpoint,
    db_connection: Connection,
    tested_code_name: str,
    code_values_file_name: str,
):
    code_values = load_code_values(code_values_file_name)

    assert (
        codes_api.get_code_by_name(tested_code_name).get("name") == tested_code_name
    ), f"Expected to find a code named '{tested_code_name}'"

    create_missing_code_values(
        codes_api=codes_api,
        db_connection=db_connection,
        code_name=tested_code_name,
        code_values=code_values,
    )

    assert_code_values_present(
        db_connection=db_connection,
        code_name=tested_code_name,
        expected_code_values=code_values,
    )
