import json
import random
from typing import Any

from colorama import Fore, Style
from rich.progress import track

from dataset.dataset_config import DatasetConfig
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.order.order_operations import OrderOperations


class OrdersGenerator(DatasetConfig):
    def __init__(self):
        super().__init__()

    def get_fixed_rate_shipping_method(self) -> dict[str, Any]:
        shipping_method = next(
            shipping_method
            for shipping_method in self.available_shipping_methods
            if shipping_method["code"] == "FixedRate"
        )

        shipping_option = random.choice(shipping_method["settings"])

        return {
            "shipmentMethodCode": shipping_method["code"],
            "shipmentMethodOption": shipping_option["name"].split(".")[-2],
            "price": shipping_option["value"],
        }

    def get_bopis_shipping_method(self) -> dict[str, Any]:
        shipping_method = next(
            shipping_method
            for shipping_method in self.available_shipping_methods
            if shipping_method["code"] == "BuyOnlinePickupInStore"
        )

        return {
            "shipmentMethodCode": shipping_method["code"],
            "shipmentMethodOption": "Pickup",
            "pickupLocationId": random.choice(self.pickup_locations)["id"],
            "price": 0,
        }

    def get_manual_payment_method(self) -> dict[str, Any]:
        payment_method = next(
            payment_method
            for payment_method in self.available_payment_methods
            if payment_method["code"] == "DefaultManualPaymentMethod"
        )

        return {
            "paymentGatewayCode": payment_method["code"],
        }

    def get_authorize_net_payment_method(self) -> dict[str, Any]:
        payment_method = next(
            payment_method
            for payment_method in self.available_payment_methods
            if payment_method["code"] == "AuthorizeNetPaymentMethod"
        )
        return {
            "paymentGatewayCode": payment_method["code"],
        }

    def generate_orders(self, count: int = 20) -> None:
        cart_operations = CartOperations(self.graphql_client)
        order_operations = OrderOperations(self.graphql_client)

        organization_address = self.organizations[0]["addresses"][0]

        orders = []
        for _ in track(range(count), description="Generating orders"):
            user = random.choice(self.users)
            currency = random.choice(self.currencies)

            items_to_add = []
            for _ in range(random.randint(1, 5)):
                product = random.choice(self.products)
                items_to_add.append(
                    {
                        "productId": product["id"],
                        "quantity": random.randint(1, 20),
                    }
                )

            cart = cart_operations.add_items_to_cart(
                {
                    "storeId": self.config["store_id"],
                    "userId": user["id"],
                    "currencyCode": currency["code"],
                    "cultureName": self.language,
                    "cartItems": items_to_add,
                }
            )

            shipment = random.choice(
                [
                    self.get_fixed_rate_shipping_method(),
                    self.get_bopis_shipping_method(),
                ]
            )
            shipment["deliveryAddress"] = {
                **organization_address,
                "addressType": 1,
            }
            cart = cart_operations.add_or_update_cart_shipment(
                {
                    "storeId": self.store_id,
                    "userId": user["id"],
                    "currencyCode": currency["code"],
                    "cultureName": self.language,
                    "shipment": shipment,
                }
            )

            payment = random.choice(
                [
                    self.get_manual_payment_method(),
                    self.get_authorize_net_payment_method(),
                ]
            )
            payment["billingAddress"] = {
                **organization_address,
                "addressType": 2,
            }
            cart = cart_operations.add_or_update_cart_payment(
                {
                    "storeId": self.store_id,
                    "userId": user["id"],
                    "currencyCode": currency["code"],
                    "cultureName": self.language,
                    "payment": payment,
                }
            )

            order = cart_operations.create_order_from_cart(
                {
                    "cartId": cart["id"],
                }
            )

            available_order_statuses = [
                "Cancelled",
                "Completed",
                "New",
                "Payment required",
                "Pending",
            ]

            if (
                "shipments" in order
                and order["shipments"][0]["shipmentMethodCode"]
                == "BuyOnlinePickupInStore"
            ):
                available_order_statuses.append("ReadyForPickup")

            order_operations.change_order_status(
                {
                    "orderId": order["id"],
                    "status": random.choice(available_order_statuses),
                }
            )

        orders = self.webapi_client.post(
            "/api/order/customerOrders/search",
            data={"storeId": self.store_id},
        )

        with open(
            self.base_dir / "data" / "orders.json", "w", encoding="utf-8"
        ) as file:
            json.dump(orders["results"], file, indent=4)

        print(Fore.GREEN + "OK" + Style.RESET_ALL)


if __name__ == "__main__":
    orders_generator = OrdersGenerator()
    orders_generator.authenticate(
        orders_generator.config["admin_username"],
        orders_generator.config["admin_password"],
    )

    orders_generator.get_available_shipping_methods()
    orders_generator.get_available_payment_methods()

    orders_generator.generate_orders(20)

    orders_generator.sign_out()
