from typing import Any, TypedDict

from api.base_endpoint import BaseEndpoint

Number = int | float


class SavingsProductPayload(TypedDict):
    name: str
    shortName: str
    description: str
    currencyCode: str
    digitsAfterDecimal: int
    inMultiplesOf: int
    nominalAnnualInterestRate: Number
    interestCompoundingPeriodType: int
    interestPostingPeriodType: int
    interestCalculationType: int
    interestCalculationDaysInYearType: int
    accountingRule: int
    minRequiredOpeningBalance: Number
    lockinPeriodFrequency: int
    lockinPeriodFrequencyType: int
    enforceMinRequiredBalance: bool
    withdrawalFeeForTransfers: bool
    paymentChannelToFundSourceMappings: list[Any]
    feeToIncomeAccountMappings: list[Any]
    penaltyToIncomeAccountMappings: list[Any]
    charges: list[Any]
    allowOverdraft: bool
    withHoldTax: bool
    isDormancyTrackingActive: bool
    lienAllowed: bool
    locale: str


class SavingsProductsEndpoint(BaseEndpoint):
    """
    An MFIs savings product offerings are modeled using this API. When creating savings accounts, the details from the savings product are used to auto fill details of the savings account application process.
    """

    def list_savings_products(
        self,
        expected_status: int = 200,
    ) -> list[Any]:
        return self._get(
            "/savingsproducts",
            expected_status,
        )

    def create_savings_product(
        self, savings_product: SavingsProductPayload, expected_status: int = 200
    ) -> dict[str, Any]:
        return self._post(
            "/savingsproducts", self._savings_product_payload(savings_product), expected_status
        )

    def _savings_product_payload(self, savings_product: SavingsProductPayload) -> dict[str, Any]:
        return dict(savings_product)
