from gql import gql
from graphql_client.types.address_validation_result_type import AddressValidationResultType


class ValidateAddressQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> AddressValidationResultType:
        query_string = f"""
            query validateAddress($storeId: String!, $customerId: String!, $address: InputAddressType!) {{
                validateAddress(
                    storeId: $storeId,
                    customerId: $customerId,
                    address: $address
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["validateAddress"]
