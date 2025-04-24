from gql import gql
from graphql_client.types.contract_connection import ContractConnection


class OrganizationContractsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ContractConnection:
        query_string = f"""
            query organizationContracts($after: String, $first: Int, $organizationId: String!, $storeId: String, $vendorId: String, $statuses: [String], $startDate: DateTime, $endDate: DateTime) {{
                organizationContracts(
                    after: $after,
                    first: $first,
                    organizationId: $organizationId,
                    storeId: $storeId,
                    vendorId: $vendorId,
                    statuses: $statuses,
                    startDate: $startDate,
                    endDate: $endDate
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["organizationContracts"]
