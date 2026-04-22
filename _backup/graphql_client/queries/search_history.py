from gql import gql
from graphql_client.types.search_history_result_type import SearchHistoryResultType


class SearchHistoryQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> SearchHistoryResultType:
        query_string = f"""
            query searchHistory($storeId: String!, $maxCount: Int!) {{
                searchHistory(
                    storeId: $storeId,
                    maxCount: $maxCount
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["searchHistory"]
