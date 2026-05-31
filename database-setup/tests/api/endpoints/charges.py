from typing import Any, NotRequired, TypedDict

from api.base_endpoint import BaseEndpoint

Number = int | float


class ChargePayload(TypedDict):
    active: bool
    amount: Number
    chargeAppliesTo: int
    chargeCalculationType: int
    chargePaymentMode: NotRequired[int]
    chargeTimeType: int
    currencyCode: str
    enablePaymentType: NotRequired[bool]
    feeFrequency: NotRequired[int]
    feeInterval: NotRequired[str]
    feeOnMonthDay: NotRequired[str]
    locale: str
    maxCap: NotRequired[Number]
    minCap: NotRequired[Number]
    monthDayFormat: NotRequired[str]
    name: str
    paymentTypeId: NotRequired[int]
    penalty: bool
    taxGroupId: NotRequired[int]


class ChargesEndpoint(BaseEndpoint):
    """
    Its typical for MFIs to add extra costs for their financial products. These are typically Fees or Penalties.

    A Charge on fineract platform is what we use to model both Fees and Penalties.

    At present we support defining charges for use with Client accounts and both loan and saving products.
    """

    def list_charges(
        self,
        expected_status: int = 200,
    ) -> list[Any]:
        return self._get(
            "/charges",
            expected_status,
        )

    def create_charge(
        self, charge: ChargePayload, expected_status: int = 200
    ) -> dict[str, Any]:
        return self._post("/charges", self._charge_payload(charge), expected_status)

    def _charge_payload(self, charge: ChargePayload) -> dict[str, Any]:
        return dict(charge)
