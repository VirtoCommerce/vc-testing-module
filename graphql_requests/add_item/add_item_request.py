from .add_item_body import ADD_ITEM


class AddItemRequest:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, store_id, user_id, product_id, quantity):
        variables = {"command": {"storeId": store_id, "userId": user_id, "productId": product_id, "quantity": quantity}}

        result = self.graphql_client.execute(ADD_ITEM, variable_values=variables)

        return result
