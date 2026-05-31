from typing import Any, TypedDict

from api.base_endpoint import BaseEndpoint

Number = int | float


class LoanProductPayload(TypedDict):
    """Payload fields accepted by the Fineract loan products API."""

    name: str
    shortName: str
    description: str
    currencyCode: str
    digitsAfterDecimal: int
    inMultiplesOf: int
    principal: Number
    numberOfRepayments: int
    repaymentEvery: int
    repaymentFrequencyType: int
    interestRatePerPeriod: Number
    interestRateFrequencyType: int
    amortizationType: int
    interestType: int
    interestCalculationPeriodType: int
    transactionProcessingStrategyCode: str
    accountingRule: int
    isInterestRecalculationEnabled: bool
    daysInYearType: int
    daysInMonthType: int
    inArrearsTolerance: Number
    includeInBorrowerCycle: bool
    useBorrowerCycle: bool
    canDefineInstallmentAmount: bool
    allowVariableInstallments: bool
    allowPartialPeriodInterestCalculation: bool
    loanScheduleType: str
    loanScheduleProcessingType: str
    repaymentStartDateType: int
    enableDownPayment: bool
    enableBuyDownFee: bool
    holdGuaranteeFunds: bool
    accountMovesOutOfNPAOnlyOnArrearsCompletion: bool
    locale: str


class LoanProductsEndpoint(BaseEndpoint):
    """
    A Loan product is a template that is used when creating a loan. Much of the template definition can be overridden during loan creation.
    """

    def list_loan_products(
        self,
        expected_status: int = 200,
    ) -> list[Any]:
        """Return loan products from the Fineract API."""
        return self._get(
            "/loanproducts",
            expected_status,
        )

    def create_loan_product(
        self, loan_product: LoanProductPayload, expected_status: int = 200
    ) -> dict[str, Any]:
        """Create a Fineract loan product from a seed payload."""
        return self._post(
            "/loanproducts", self._loan_product_payload(loan_product), expected_status
        )

    def _loan_product_payload(self, loan_product: LoanProductPayload) -> dict[str, Any]:
        """Convert a typed loan product payload to a mutable request body."""
        return dict(loan_product)
