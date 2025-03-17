import allure
from tests_graphql.pages.orders.orders_page import OrdersPage
from tests_graphql.test_data.orders_test_data import OrdersTestData


@allure.title("Get Full Order Details (GraphQL)")
def test_get_full_order(graphql_client):
    """Test retrieving and verifying full order details"""
    # Initialize the orders page
    orders_page = OrdersPage(graphql_client)
    
    # Get and verify order details
    order = orders_page.get_full_order(OrdersTestData.TEST_ORDER_ID)
    
    # Verify different aspects of the order
    orders_page.verify_order_items(order)
    orders_page.verify_order_addresses(order)
    orders_page.verify_order_totals(order)
    
    # Verify specific expected values
    assert order["status"] == OrdersTestData.EXPECTED_STATUS, "Unexpected order status" 