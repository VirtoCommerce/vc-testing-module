from gql import gql
from graphql_client.types.bulletin_board_result_type import BulletinBoardResultType


class UpdateBulletinBoardMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> BulletinBoardResultType:
        query_string = f"""
            mutation updateBulletinBoard($command: InputUpdateBulletinBoardType!) {{
                updateBulletinBoard(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["updateBulletinBoard"]
