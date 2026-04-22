from gql import gql
from graphql_client.types.payment_in_connection import PaymentInConnection


class PaymentsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> PaymentInConnection:
        query_string = f"""
            query payments($facet: String, $filter: String, $sort: String, $cultureName: String, $userId: String, $after: String, $first: Int) {{
                payments(
                    facet: $facet,
                    filter: $filter,
                    sort: $sort,
                    cultureName: $cultureName,
                    userId: $userId,
                    after: $after,
                    first: $first
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["payments"]
