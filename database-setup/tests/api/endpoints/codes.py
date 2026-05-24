from typing import Any

from api.base_endpoint import BaseEndpoint


class CodesEndpoint(BaseEndpoint):
    """
    Code and code values: Codes represent a specific category of data, their code values are a specific instance of that category.

    Codes are mostly system defined which means the code itself comes out of the box and cannot be modified however its code values can be. e.g. 'Customer Identifier',
    it defaults to a code value of 'Passport' but could be 'Drivers License, National Id' etc
    """

    def list_codes(self, expected_status: int = 200) -> list[Any]:
        return self._get("/codes", expected_status)

    def get_code_by_name(
        self, code_name: str, expected_status: int = 200
    ) -> dict[str, Any]:
        return self._get(f"/codes/name/{code_name}", expected_status)

    def get_code_values(self, code_id: int, expected_status: int = 200) -> list[Any]:
        return self._get(f"/codes/{code_id}/codevalues", expected_status)

    def create_code_values_by_id(
        self, code_id: int, code_value: dict[str, Any], expected_status: int = 200
    ) -> dict[str, Any]:
        return self._post(f"/codes/{code_id}/codevalues", code_value, expected_status)

    def create_code_values_by_name(
        self, code_name: str, code_value: dict[str, Any], expected_status: int = 200
    ) -> dict[str, Any]:
        return self._post(
            f"/codes/name/{code_name}/codevalues", code_value, expected_status
        )
