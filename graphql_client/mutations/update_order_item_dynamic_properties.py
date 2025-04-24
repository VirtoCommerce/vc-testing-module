from gql import gql
from graphql_client.types.customer_order_type import CustomerOrderType


class UpdateOrderItemDynamicPropertiesMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CustomerOrderType:
        query_string = f"""
            mutation updateOrderItemDynamicProperties($command: InputUpdateOrderItemDynamicPropertiesType!) {{
                updateOrderItemDynamicProperties(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["updateOrderItemDynamicProperties"]
