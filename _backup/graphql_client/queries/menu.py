from gql import gql
from graphql_client.types.menu_link_list_type import MenuLinkListType


class MenuQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> MenuLinkListType:
        query_string = f"""
            query menu($storeId: String!, $cultureName: String!, $name: String!) {{
                menu(
                    storeId: $storeId,
                    cultureName: $cultureName,
                    name: $name
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["menu"]
