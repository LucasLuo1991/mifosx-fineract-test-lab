from typing import Any, Literal, TypedDict

from api.base_endpoint import BaseEndpoint

StaffStatus = Literal["active", "inactive"]


class StaffPayload(TypedDict):
    """Payload fields accepted by the Fineract staff API and DB assertions."""

    dateFormat: str
    emailAddress: str
    externalId: str
    firstname: str
    isActive: bool
    isLoanOfficer: bool
    joiningDate: str
    lastname: str
    locale: str
    mobileNo: str
    officeId: int
    display_name: str # This field is not part of the API payload but is used for testing purposes to identify staff members by their display name.


class StaffEndpoint(BaseEndpoint):
    """
    Allows you to model staff members. At present the key role of significance is whether this staff member is a loan officer or not.
    """

    def list_staff(
        self,
        expected_status: int = 200,
        office_id: int | None = None,
        staff_in_office_hierarchy: bool | None = None,
        loan_officers_only: bool | None = None,
        status: StaffStatus | None = None,
    ) -> list[Any]:
        """Return staff from the Fineract API using optional filters."""
        return self._get(
            "/staff",
            expected_status,
            params=self._list_staff_params(
                office_id=office_id,
                staff_in_office_hierarchy=staff_in_office_hierarchy,
                loan_officers_only=loan_officers_only,
                status=status,
            ),
        )

    def create_staff(
        self, staff: StaffPayload, expected_status: int = 200
    ) -> dict[str, Any]:
        """Create a Fineract staff member from a seed payload."""
        return self._post("/staff", self._staff_payload(staff), expected_status)

    def _list_staff_params(
        self,
        office_id: int | None = None,
        staff_in_office_hierarchy: bool | None = None,
        loan_officers_only: bool | None = None,
        status: StaffStatus | None = None,
    ) -> dict[str, Any]:
        """Build query parameters for listing staff."""

        params: dict[str, Any] = {}

        if office_id is not None:
            params["officeId"] = office_id
        if staff_in_office_hierarchy is not None:
            params["staffInOfficeHierarchy"] = str(staff_in_office_hierarchy).lower()
        if loan_officers_only is not None:
            params["loanOfficersOnly"] = str(loan_officers_only).lower()
        if status is not None:
            params["status"] = status

        return params

    def _staff_payload(self, staff: StaffPayload) -> dict[str, Any]:
        """Remove test-only fields from a typed staff payload."""
        payload = dict(staff)
        payload.pop("display_name", None)  # Remove the display_name key as it's not part of the API payload
        return payload
