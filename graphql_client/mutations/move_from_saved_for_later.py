from gql import gql
from graphql_client.types.cart_with_list_type import CartWithListType


class MoveFromSavedForLaterMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CartWithListType:
        query_string = f"""
            mutation moveFromSavedForLater($command: InputSaveForLaterType!) {{
                moveFromSavedForLater(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["moveFromSavedForLater"]
