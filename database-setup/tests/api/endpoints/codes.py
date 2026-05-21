from api.base_endpoint import BaseEndpoint


class CodesEndpoint(BaseEndpoint):
    """
    Code and code values: Codes represent a specific category of data, their code values are a specific instance of that category.

    Codes are mostly system defined which means the code itself comes out of the box and cannot be modified however its code values can be. e.g. 'Customer Identifier',
    it defaults to a code value of 'Passport' but could be 'Drivers License, National Id' etc
    """

    def get_all_codes(self):
        return self._get("/codes")
