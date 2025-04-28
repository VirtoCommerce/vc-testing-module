from gql import gql
from graphql_client.types.customer_order_connection import CustomerOrderConnection


class OrganizationOrdersQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CustomerOrderConnection:
        query_string = f"""
            query organizationOrders($after: String, $first: Int, $sort: String, $facet: String, $filter: String, $cultureName: String, $organizationId: String) {{
                organizationOrders(
                    after: $after,
                    first: $first,
                    sort: $sort,
                    facet: $facet,
                    filter: $filter,
                    cultureName: $cultureName,
                    organizationId: $organizationId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["organizationOrders"]
