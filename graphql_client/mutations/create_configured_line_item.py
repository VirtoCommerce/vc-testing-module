from gql import gql
from graphql_client.types.configuration_line_item_type import ConfigurationLineItemType


class CreateConfiguredLineItemMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ConfigurationLineItemType:
        query_string = f"""
            mutation createConfiguredLineItem($command: InputCreateConfiguredLineItemCommand!) {{
                createConfiguredLineItem(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["createConfiguredLineItem"]
