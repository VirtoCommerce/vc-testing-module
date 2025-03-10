import allure

from e2e.graphql.client import add_item


class GraphQLSteps:
    def __init__(self, graphql_client, user_id):
        self.graphql_client = graphql_client
        self.user_id = user_id

    @allure.step("Add product to cart (GraphQL)")
    def add_product_to_cart(self, product_id, quantity, item_id):
        result = add_item(self.graphql_client, self.user_id, product_id, quantity)
        assert result["addItem"]["id"] == item_id
