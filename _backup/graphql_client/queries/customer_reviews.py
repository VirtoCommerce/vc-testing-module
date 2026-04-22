from gql import gql
from graphql_client.types.customer_review_connection import CustomerReviewConnection


class CustomerReviewsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CustomerReviewConnection:
        query_string = f"""
            query customerReviews($after: String, $first: Int, $keyword: String, $sort: String, $storeId: String!, $entityId: String!, $entityType: String!, $filter: String) {{
                customerReviews(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    storeId: $storeId,
                    entityId: $entityId,
                    entityType: $entityType,
                    filter: $filter
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["customerReviews"]
