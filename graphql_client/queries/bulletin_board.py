from gql import gql
from graphql_client.types.bulletin_board_type import BulletinBoardType


class BulletinBoardQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> BulletinBoardType:
        query_string = f"""
            query bulletinBoard($storeId: String!, $userId: String!) {{
                bulletinBoard(
                    storeId: $storeId,
                    userId: $userId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["bulletinBoard"]
