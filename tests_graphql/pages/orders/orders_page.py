import allure
from gql import Client
from graphql_requests.get_full_order.get_full_order_request import GetFullOrderRequest


class OrdersPage:
    def __init__(self, client: Client):
        self.client = client
        self.get_order_request = GetFullOrderRequest(client)

    @allure.step("Get full order details")
    def get_full_order(self, order_id: str) -> dict:
        """
        Get full order details and verify the response structure
        
        Args:
            order_id: The ID of the order to retrieve
            
        Returns:
            dict: Verified order details
        """
        result = self.get_order_request.execute(order_id)
        order = result["order"]
        
        # Verify basic order structure
        assert order["id"] == order_id, "Order ID mismatch"
        assert order["status"] is not None, "Order status is missing"
        assert order["items"] is not None, "Order items are missing"
        
        return order

    @allure.step("Verify order items")
    def verify_order_items(self, order: dict):
        """Verify order items data"""
        assert order["items"], "Order has no items"
        
        for item in order["items"]:
            assert item["sku"], "Item SKU is missing"
            assert item["quantity"] > 0, "Invalid item quantity"
            assert float(item["price"]["amount"]) > 0, "Invalid item price"
            assert item["name"], "Item name is missing"

    @allure.step("Verify order addresses")
    def verify_order_addresses(self, order: dict):
        """Verify shipping and billing addresses"""
        addresses = order["addresses"]
        assert addresses, "Order addresses are missing"
        
        for address in addresses:
            assert address["firstName"], "Address first name is missing"
            assert address["lastName"], "Address last name is missing"           
            assert address["line1"], "Address line 1 is missing"
            assert address["city"], "Address city is missing"
            assert address["addressType"], "Address type is missing"

    @allure.step("Verify order totals")
    def verify_order_totals(self, order: dict):
        """Verify order total amounts"""
        assert float(order["total"]["amount"]) > 0, "Invalid order total"
        assert float(order["subTotal"]["amount"]) > 0, "Invalid order subtotal"
        assert float(order["shippingTotal"]["amount"]) >= 0, "Invalid shipping total"
        assert float(order["taxTotal"]["amount"]) >= 0, "Invalid tax total"
        assert float(order["paymentTotal"]["amount"]) >= 0, "Invalid payment total"
        assert order["total"]["formattedAmount"], "Formatted total amount is missing" 