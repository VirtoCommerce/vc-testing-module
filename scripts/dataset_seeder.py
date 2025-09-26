import json
import os
import random
import uuid
from typing import Any, Dict

from colorama import Fore, Style
from colorama import init as init_colorama
from dotenv import load_dotenv
from gql.transport.requests import RequestsHTTPTransport

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from fixtures.webapi_client import WebAPISession
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.order.order_operations import OrderOperations


class DatasetSeeder:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.auth = Auth(config)
        self.webapi_client = WebAPISession(config, self.auth)
        self.transport = RequestsHTTPTransport(
            url=f"{config['backend_base_url']}/graphql",
            headers={"Content-Type": "application/json"},
            use_json=True,
            verify=True,
        )
        self.graphql_client = GraphQLClient(self.transport, self.auth)
        self.dataset = None
        self.store_id = config["store_id"]

    def get_file_path(self, file_name: str) -> str:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file_name)

        return file_path

    def authenticate(self, username: str, password: str) -> None:
        self.auth.authenticate(username, password)

    def sign_out(self) -> None:
        self.auth.clear_token()

    def fetch_dataset(self, file_path: str) -> None:
        with open(self.get_file_path(file_path), "r", encoding="utf-8") as file:
            self.dataset = json.load(file)

    def create_languages(self) -> None:
        if not self.dataset["languages"]:
            raise ValueError("No languages found in dataset")

        for language in self.dataset["languages"]:
            print(f'Creating language "{language}"...', end=" ")

            default_culture = self.dataset["languages"][0]

            self.webapi_client.post(
                "/api/platform/settings",
                data=[
                    {
                        "allowedValues": self.dataset["languages"],
                        "defaultValue": default_culture,
                        "groupName": "General",
                        "isDictionary": True,
                        "isHasValues": True,
                        "moduleId": "Platform",
                        "name": "VirtoCommerce.Core.General.Languages",
                        "translatedName": "Languages",
                        "value": default_culture,
                        "valueType": "ShortText",
                    }
                ],
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_currencies(self) -> None:
        if not self.dataset["currencies"]:
            raise ValueError("No currencies found in dataset")

        for currency in self.dataset["currencies"]:
            print(f'Creating currency "{currency["code"]}"...', end=" ")

            self.webapi_client.post(
                "/api/currencies",
                data=currency,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_measures(self) -> None:
        if not self.dataset["measures"]:
            raise ValueError("No measures found in dataset")

        for measure in self.dataset["measures"]:
            print(f'Creating measure "{measure["name"]}"...', end=" ")
            self.webapi_client.put(
                "/api/catalog/measures",
                data=measure,
            )
            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_fulfillment_centers(self) -> None:
        if not self.dataset["fulfillmentCenters"]:
            raise ValueError("No fulfillment centers found in dataset")

        for ffc in self.dataset["fulfillmentCenters"]:
            print(f'Creating fulfillment center "{ffc["name"]}"...', end=" ")

            self.webapi_client.put(
                "/api/inventory/fulfillmentcenters",
                data=ffc,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_pricelists(self) -> None:
        if not self.dataset["pricelists"]:
            raise ValueError("No pricelists found in dataset")

        for pricelist in self.dataset["pricelists"]:
            print(f'Creating pricelist "{pricelist["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/pricing/pricelists",
                data=pricelist,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_pricelist_assignments(self) -> None:
        if not self.dataset["pricelistAssignments"]:
            raise ValueError("No pricelist assignments found in dataset")

        for pricelist_assignment in self.dataset["pricelistAssignments"]:
            print(
                f'Creating pricelist assignment "{pricelist_assignment["name"]}"...',
                end=" ",
            )

            self.webapi_client.post(
                "/api/pricing/assignments",
                data=pricelist_assignment,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_catalogs(self) -> None:
        if not self.dataset["catalogs"]:
            raise ValueError("No catalogs found in dataset")

        for catalog in self.dataset["catalogs"]:
            print(f'Creating catalog "{catalog["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/catalog/catalogs",
                data=catalog,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_property_groups(self) -> None:
        if not self.dataset["propertyGroups"]:
            raise ValueError("No property groups found in dataset")

        for property_group in self.dataset["propertyGroups"]:
            print(f'Creating property group "{property_group["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/catalog/propertygroups",
                data=property_group,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_properties(self) -> None:
        if not self.dataset["properties"]:
            raise ValueError("No properties found in dataset")

        for property in self.dataset["properties"]:
            print(
                f'Creating property "{property["name"]}"...',
                end=" ",
            )

            self.webapi_client.post(
                f"/api/catalog/properties?id={property['id']}",
                data=property,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_stores(self) -> None:
        if not self.dataset["stores"]:
            raise ValueError("No stores found in dataset")

        for store in self.dataset["stores"]:
            print(f'Creating store "{store["name"]}"...', end=" ")

            store["url"] = f"{self.config['frontend_base_url']}"

            self.webapi_client.post(
                "/api/stores",
                data=store,
            )   

          
            payment_methods = self.webapi_client.post(
                "/api/payment/search", data={"storeId": self.store_id}
            )["results"]

            shipping_methods = self.webapi_client.post(
                "/api/shipping/search", data={"storeId": self.store_id}
            )["results"]

            for payment_method in payment_methods:
                payment_method["isActive"] = True
                self.webapi_client.put("/api/payment", data=payment_method)

            for shipping_method in shipping_methods:
                shipping_method["isActive"] = True
                if shipping_method["code"] == "FixedRate":
                    shipping_method["settings"] = [
                        {
                            "groupName": "General",
                            "objectId": shipping_method["id"],
                            "objectType": "FixedRateShippingMethod",
                            "moduleId": "VirtoCommerce.Shipping",
                            "name": "VirtoCommerce.Shipping.FixedRateShippingMethod.Ground.Rate",
                            "value": 15.00,
                            "valueType": "Decimal",
                        },
                        {
                            "groupName": "General",
                            "objectId": shipping_method["id"],
                            "objectType": "FixedRateShippingMethodOption",
                            "moduleId": "VirtoCommerce.Shipping",
                            "name": "VirtoCommerce.Shipping.FixedRateShippingMethod.Air.Rate",
                            "value": 35.00,
                            "valueType": "Decimal",
                        },
                    ]
                self.webapi_client.put("/api/shipping", data=shipping_method)

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_aggregation_properties(self) -> None:
        if not self.dataset["aggregationProperties"]:
            raise ValueError("No aggregation properties found in dataset")

        if not self.store_id:
            raise ValueError("Store ID not found")

        print(f"Creating aggregation properties...", end=" ")

        self.webapi_client.put(
            f"/api/catalog/aggregationproperties/{self.store_id}/properties",
            data=self.dataset["aggregationProperties"],
        )

        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_categories(self) -> None:
        if not self.dataset["categories"]:
            raise ValueError("No categories found in dataset")

        for category in self.dataset["categories"]:
            print(f'Creating category "{category["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/catalog/categories",
                data=category,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_products(self) -> None:
        if not self.dataset["products"]:
            raise ValueError("No products found in dataset")

        for product in self.dataset["products"]:
            print(f'Creating product "{product["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/catalog/products",
                data=product,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_products_inventories(self) -> None:
        if not self.dataset["productsInventories"]:
            raise ValueError("No products inventories found in dataset")

        for product_inventory in self.dataset["productsInventories"]:
            print(
                f'Creating product inventory "{product_inventory["fulfillmentCenterName"]} -> {product_inventory["productName"]}"...',
                end=" ",
            )

            self.webapi_client.put(
                f"/api/inventory/products/{product_inventory['productId']}",
                data=product_inventory,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_prices(self) -> None:
        if not self.dataset["prices"]:
            raise ValueError("No prices found in dataset")

        for price in self.dataset["prices"]:
            print(
                f'Creating price for product "{price["product"]["name"]}"...',
                end=" ",
            )

            self.webapi_client.put(
                f"/api/products/{price['productId']}/prices",
                data=price,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_promotions(self) -> None:
        if not self.dataset["promotions"]:
            raise ValueError("No promotions found in dataset")

        for promotion in self.dataset["promotions"]:
            print(f'Creating promotion "{promotion["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/marketing/promotions",
                data=promotion,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_coupons(self) -> None:
        if not self.dataset["coupons"]:
            return

        print(f'Creating coupons"...', end=" ")

        self.webapi_client.post(
            "/api/marketing/promotions/coupons/add",
            data=self.dataset["coupons"],
        )

        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_roles(self) -> None:
        if not self.dataset["roles"]:
            raise ValueError("No roles found in dataset")

        for role in self.dataset["roles"]:
            print(f'Creating role "{role["name"]}"...', end=" ")

            self.webapi_client.put(
                "/api/platform/security/roles",
                data=role,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_organizations(self) -> None:
        if not self.dataset["organizations"]:
            raise ValueError("No organizations found in dataset")

        for organization in self.dataset["organizations"]:
            print(f'Creating organization "{organization["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/members",
                data=organization,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_contacts(self) -> None:
        if not self.dataset["contacts"]:
            raise ValueError("No contacts found in dataset")

        for contact in self.dataset["contacts"]:
            print(
                f'Creating contact "{contact["firstName"]} {contact["lastName"]}"...',
                end=" ",
            )

            self.webapi_client.post(
                "/api/members",
                data=contact,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_users(self) -> None:
        if not self.dataset["users"]:
            raise ValueError("No users found in dataset")

        for user in self.dataset["users"]:
            print(f'Creating user "{user["userName"]}"...', end=" ")

            user["password"] = self.config["users_password"]
            self.webapi_client.post(
                "/api/platform/security/users/create",
                data=user,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def rebuild_index(self, document_type: str, delete_existing: bool = True) -> None:
        print(f"Rebuilding index {document_type}...", end=" ")
        payload = [
            {
                "deleteExisting": delete_existing,
                "documentType": document_type,
            }
        ]
        self.webapi_client.post("/api/search/indexes/index", data=payload)
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    """
    def create_orders(self, count: int = 50) -> None:
        print(f"Creating {count} order(s)...", end=" ")

        cart_operations = CartOperations(self.graphql_client)
        order_operations = OrderOperations(self.graphql_client)

        for _ in range(count):
            contact = random.choice(self.dataset["contacts"])
            user = next(
                user
                for user in self.dataset["users"]
                if user["memberId"] == contact["id"]
            )
            product = random.choice(
                [
                    product
                    for product in self.dataset["products"]
                    if product["id"]
                    == random.choice(
                        [
                            product_inventory["productId"]
                            for product_inventory in self.dataset["productsInventories"]
                            if product_inventory["inStockQuantity"] > "0"
                        ]
                    )
                ]
            )

            cart = cart_operations.add_item_to_cart(
                payload={
                    "storeId": self.store_id,
                    "userId": user["id"],
                    "productId": product["id"],
                    "quantity": random.randint(1, 20),
                    "currencyCode": self.dataset["currencies"][0]["code"],
                    "cultureName": self.dataset["languages"][0],
                }
            )

            cart_operations.add_or_update_cart_shipment(
                payload={
                    "storeId": self.store_id,
                    "userId": user["id"],
                    "currencyCode": self.dataset["currencies"][0]["code"],
                    "cultureName": self.dataset["languages"][0],
                    "shipment": {
                        "shipmentMethodCode": "FixedRate",
                        "shipmentMethodOption": "Ground",
                        "price": random.randint(10, 100),
                    },
                }
            )
            cart_operations.add_or_update_cart_payment(
                payload={
                    "storeId": self.store_id,
                    "userId": user["id"],
                    "currencyCode": self.dataset["currencies"][0]["code"],
                    "cultureName": self.dataset["languages"][0],
                    "payment": {
                        "paymentGatewayCode": "DefaultManualPaymentMethod",
                        "price": 0,
                    },
                }
            )

            order = cart_operations.create_order_from_cart(
                payload={
                    "cartId": cart["id"],
                }
            )

            order_operations.change_order_status(
                payload={
                    "orderId": order["id"],
                    "status": random.choice(
                        [
                            "Cancelled",
                            "Completed",
                            "New",
                            "Not payed",
                            "Pending",
                            "Processing",
                        ]
                    ),
                }
            )

        print(Fore.GREEN + "OK" + Style.RESET_ALL)
    """


def get_config():
    load_dotenv(override=True)

    return {
        "backend_base_url": os.getenv("BACKEND_BASE_URL"),
        "frontend_base_url": os.getenv("FRONTEND_BASE_URL"),
        "store_id": os.getenv("STORE_ID"),
        "admin_username": os.getenv("ADMIN_USERNAME"),
        "admin_password": os.getenv("ADMIN_PASSWORD"),
        "users_password": os.getenv("USERS_PASSWORD"),
    }


if __name__ == "__main__":
    init_colorama()

    config = get_config()

    seeder = DatasetSeeder(config)
    seeder.authenticate(config["admin_username"], config["admin_password"])

    seeder.fetch_dataset("dataset.json")

    seeder.create_languages()
    seeder.create_currencies()
    seeder.create_fulfillment_centers()
    seeder.create_measures()
    seeder.create_catalogs()
    seeder.create_property_groups()
    seeder.create_stores()   
    seeder.create_pricelists()
    seeder.create_pricelist_assignments()
    seeder.create_categories()
    seeder.create_properties()
    seeder.create_aggregation_properties()
    seeder.create_products()
    seeder.create_products_inventories()
    seeder.create_prices()
    seeder.create_promotions()
    seeder.create_coupons()
    seeder.create_roles()
    seeder.create_organizations()
    seeder.create_contacts()
    seeder.create_users()

    seeder.rebuild_index("Member")
    seeder.rebuild_index("Product")
    seeder.rebuild_index("Category")
    seeder.rebuild_index("ContentFile")
    seeder.rebuild_index("CustomerOrder")

    seeder.sign_out()
