from graphql_requests.add_item.add_item_request import AddItemRequest
from graphql_requests.create_order_from_cart.create_order_from_cart_request import CreateOrderFromCartRequest
from tests_graphql.test_data.test_store import TEST_STORE as test_store
from tests_graphql.test_data.test_product import TEST_PRODUCT as test_product
from tests_graphql.test_data.test_user import TEST_PERMANENT_USER as test_user


class CreateOrderFromCartOperations:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client
        self.cart_id = None
        self.test_product_quantity = 2

    def add_item_to_cart(self):
        addItemRequest = AddItemRequest(self.graphql_client)

        result = addItemRequest.execute(
            store_id=test_store["id"],
            user_id=test_user["id"],
            product_id=test_product["id"],
            quantity=self.test_product_quantity,
        )

        self.cart_id = result["addItem"]["id"]

        cart_product = next(
            (item for item in result["addItem"]["items"] if item["productId"] == test_product["id"]), None
        )

        assert result["addItem"]["id"] is not None
        assert result["addItem"]["items"] is not None
        assert cart_product["quantity"] == self.test_product_quantity

    def create_order_from_cart(self):
        createOrderFromCartRequest = CreateOrderFromCartRequest(self.graphql_client)

        result = createOrderFromCartRequest.execute(self.cart_id)

        order_product = next(
            (item for item in result["createOrderFromCart"]["items"] if item["productId"] == test_product["id"]), None
        )

        assert result["createOrderFromCart"]["id"] is not None
        assert result["createOrderFromCart"]["number"] is not None
        assert result["createOrderFromCart"]["items"] is not None
        assert order_product["quantity"] == self.test_product_quantity
