from gql import gql
from graphql_client.types.opus_cart_type import OpusCartType


class CopyShipmentToOthersMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> OpusCartType:
        query_string = f"""
            mutation copyShipmentToOthers($command: InputCopyShipmentToOthersType!) {{
                copyShipmentToOthers(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["copyShipmentToOthers"]
