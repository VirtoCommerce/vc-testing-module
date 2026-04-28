from gql import gql
from graphql_client.types.push_message_connection import PushMessageConnection


class PushMessagesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> PushMessageConnection:
        query_string = f"""
            query pushMessages($after: String, $first: Int, $keyword: String, $sort: String, $unreadOnly: Boolean, $withHidden: Boolean, $cultureName: String) {{
                pushMessages(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    unreadOnly: $unreadOnly,
                    withHidden: $withHidden,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["pushMessages"]
