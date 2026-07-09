from typing import Any, Literal, TypedDict

from api.base_endpoint import BaseEndpoint

OfficeOrderBy = Literal["id", "name", "externalId", "openingDate", "parentId"]
SortOrder = Literal["asc", "desc"]


class OfficePayload(TypedDict):
    """Payload fields accepted by the Fineract offices API."""

    name: str
    parentId: int
    openingDate: str
    locale: str
    dateFormat: str
    externalId: str


class OfficesEndpoint(BaseEndpoint):
    """
    Offices are used to model an MFIs structure. A hierarchical representation of offices is supported.
    There will always be at least one office (which represents the MFI or an MFIs head office). All subsequent offices added must have a parent office.
    """

    def list_offices(
        self,
        expected_status: int = 200,
        include_all_offices: bool | None = None,
        order_by: OfficeOrderBy | None = None,
        sort_order: SortOrder | None = None,
    ) -> list[Any]:
        """Return offices from the Fineract API using optional filters."""
        return self._get(
            "v1/offices",
            expected_status,
            params=self._list_offices_params(
                include_all_offices=include_all_offices,
                order_by=order_by,
                sort_order=sort_order,
            ),
        )

    def create_office(
        self, office: OfficePayload, expected_status: int = 200
    ) -> dict[str, Any]:
        """Create a Fineract office from a seed payload."""
        return self._post("v1/offices", self._office_payload(office), expected_status)

    def _list_offices_params(
        self,
        include_all_offices: bool | None = None,
        order_by: OfficeOrderBy | None = None,
        sort_order: SortOrder | None = None,
    ) -> dict[str, str]:
        """Build query parameters for listing offices."""

        params: dict[str, str] = {}

        if include_all_offices is not None:
            params["includeAllOffices"] = str(include_all_offices).lower()
        if order_by is not None:
            params["orderBy"] = order_by
        if sort_order is not None:
            params["sortOrder"] = sort_order

        return params

    def _office_payload(self, office: OfficePayload) -> dict[str, Any]:
        """Convert a typed office payload to a mutable request body."""
        return dict(office)
