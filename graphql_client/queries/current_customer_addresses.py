from gql import gql
from graphql_client.types.member_address_connection import MemberAddressConnection


class CurrentCustomerAddressesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> MemberAddressConnection:
        query_string = f"""
            query currentCustomerAddresses(
                $after: String,
                $first: Int,
                $countryCodes: [String],
                $regionIds: [String],
                $cities: [String],
                $keyword: String,
                $sort: String
            ) {{
                currentCustomerAddresses(
                    after: $after,
                    first: $first,
                    countryCodes: $countryCodes,
                    regionIds: $regionIds,
                    cities: $cities,
                    keyword: $keyword,
                    sort: $sort
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["currentCustomerAddresses"]
