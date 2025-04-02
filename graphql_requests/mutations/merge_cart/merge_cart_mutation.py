from gql import Client
from .merge_cart_body import MERGE_CART


class MergeCartMutation:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def execute(
        self,
        store_id: str,
        user_id: str,
        currency_code: str,
        culture_name: str,
        second_cart_id: str,
        delete_after_merge: bool = False,
    ):
        variables = {
            "command": {
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
                "secondCartId": second_cart_id,
                "deleteAfterMerge": delete_after_merge,
            }
        }

        response = self.graphql_client.execute(MERGE_CART, variable_values=variables)

        return response
