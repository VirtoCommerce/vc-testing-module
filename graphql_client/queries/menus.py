from gql import gql
from graphql_client.types.menu_link_list_type import MenuLinkListType


class MenusQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> list[MenuLinkListType]:
        query_string = f"""
            query menus($storeId: String!, $cultureName: String, $keyword: String) {{
                menus(
                    storeId: $storeId,
                    cultureName: $cultureName,
                    keyword: $keyword
                )
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["menus"]
