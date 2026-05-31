from typing import Any, TypedDict

from api.base_endpoint import BaseEndpoint


class CodeValuePayload(TypedDict):
    name: str
    description: str
    position: int
    isActive: bool


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
        self, code_id: int, code_value: CodeValuePayload, expected_status: int = 200
    ) -> dict[str, Any]:
        return self._post(
            f"/codes/{code_id}/codevalues",
            self._code_value_payload(code_value),
            expected_status,
        )

    def create_code_values_by_name(
        self, code_name: str, code_value: CodeValuePayload, expected_status: int = 200
    ) -> dict[str, Any]:
        return self._post(
            f"/codes/name/{code_name}/codevalues",
            self._code_value_payload(code_value),
            expected_status,
        )

    def update_code_values_by_name(
        self,
        code_name: str,
        code_value_id: int,
        code_value: CodeValuePayload,
        expected_status: int = 200,
    ) -> dict[str, Any]:
        return self._put(
            f"/codes/name/{code_name}/codevalues/{code_value_id}",
            self._code_value_payload(code_value),
            expected_status,
        )

    def _code_value_payload(self, code_value: CodeValuePayload) -> dict[str, Any]:
        return dict(code_value)
