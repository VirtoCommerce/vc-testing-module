from gql import gql
from graphql_client.types.customer_order_connection import CustomerOrderConnection


class OrdersQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CustomerOrderConnection:
        query_string = f"""
            query orders($after: String, $first: Int, $sort: String, $facet: String, $filter: String, $cultureName: String, $userId: String) {{
                orders(
                    after: $after,
                    first: $first,
                    sort: $sort,
                    facet: $facet,
                    filter: $filter,
                    cultureName: $cultureName,
                    userId: $userId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["orders"]
