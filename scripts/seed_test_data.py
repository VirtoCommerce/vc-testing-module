import json
import os
from typing import Any, Dict, List

from colorama import Fore, Style
from colorama import init as init_colorama
from dotenv import load_dotenv

from fixtures import Auth, WebAPISession


class TestDataSeeder:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.auth = Auth(config)
        self.webapi_client = WebAPISession(config, self.auth)
        self.test_data = None

    def authenticate(self, username: str, password: str) -> None:
        self.auth.authenticate(username, password)

    def clear_token(self) -> None:
        self.auth.clear_token()

    def load_test_data(self, file_path: str) -> None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        test_data_file_path = os.path.join(script_dir, file_path)

        with open(test_data_file_path, "r") as file:
            self.test_data = json.load(file)

    def create_currencies(self) -> None:
        if not self.test_data["currencies"]:
            raise ValueError("No currencies found in test data")

        for currency in self.test_data["currencies"]:
            print(f'Creating currency "{currency["code"]}"...', end=" ")

            self.webapi_client.post(
                "/api/currencies",
                data=currency,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_fulfillment_centers(self) -> None:
        if not self.test_data["fulfillmentCenters"]:
            raise ValueError("No fulfillment centers found in test data")

        for ffc in self.test_data["fulfillmentCenters"]:
            print(f'Creating fulfillment center "{ffc["name"]}"...', end=" ")

            self.webapi_client.put(
                "/api/inventory/fulfillmentcenters",
                data=ffc,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_pricelists(self) -> None:
        if not self.test_data["pricelists"]:
            raise ValueError("No pricelists found in test data")

        for pricelist in self.test_data["pricelists"]:
            print(f'Creating pricelist "{pricelist["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/pricing/pricelists",
                data=pricelist,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_pricelist_assignments(self) -> None:
        if not self.test_data["pricelistAssignments"]:
            raise ValueError("No pricelist assignments found in test data")

        for pricelist_assignment in self.test_data["pricelistAssignments"]:
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
        if not self.test_data["catalogs"]:
            raise ValueError("No catalogs found in test data")

        for catalog in self.test_data["catalogs"]:
            print(f'Creating catalog "{catalog["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/catalog/catalogs",
                data=catalog,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_catalog_properties(self) -> None:
        if not self.test_data["catalogProperties"]:
            raise ValueError("No catalog properties found in test data")

        for catalog_property in self.test_data["catalogProperties"]:
            print(
                f'Creating catalog property "{catalog_property["name"]}"...',
                end=" ",
            )

            self.webapi_client.post(
                f"/api/catalog/properties?id={catalog_property['id']}",
                data=catalog_property,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_stores(self) -> None:
        if not self.test_data["stores"]:
            raise ValueError("No stores found in test data")

        for store in self.test_data["stores"]:
            print(f'Creating store "{store["name"]}"...', end=" ")

            store["url"] = f"{self.config['frontend_base_url']}"

            self.webapi_client.post(
                "/api/stores",
                data=store,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_categories(self) -> None:
        if not self.test_data["categories"]:
            raise ValueError("No categories found in test data")

        for category in self.test_data["categories"]:
            print(f'Creating category "{category["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/catalog/categories",
                data=category,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_products(self) -> None:
        if not self.test_data["products"]:
            raise ValueError("No products found in test data")

        for product in self.test_data["products"]:
            print(f'Creating product "{product["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/catalog/products",
                data=product,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_products_inventories(self) -> None:
        if not self.test_data["productsInventories"]:
            raise ValueError("No products inventories found in test data")

        for product_inventory in self.test_data["productsInventories"]:
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
        if not self.test_data["prices"]:
            raise ValueError("No prices found in test data")

        for price in self.test_data["prices"]:
            print(
                f'Creating price for product "{price["product"]["name"]}"...', end=" "
            )

            self.webapi_client.put(
                f"/api/products/{price['productId']}/prices",
                data=price,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)


def get_config():
    load_dotenv(override=True)

    return {
        "backend_base_url": os.getenv("BACKEND_BASE_URL"),
        "frontend_base_url": os.getenv("FRONTEND_BASE_URL"),
        "store_id": os.getenv("STORE_ID"),
        "admin_username": os.getenv("ADMIN_USERNAME"),
        "admin_password": os.getenv("ADMIN_PASSWORD"),
    }


if __name__ == "__main__":
    config = get_config()

    seeder = TestDataSeeder(config)
    seeder.authenticate(config["admin_username"], config["admin_password"])

    seeder.load_test_data("test_data.json")

    seeder.create_currencies()
    seeder.create_fulfillment_centers()
    seeder.create_catalogs()
    seeder.create_catalog_properties()
    seeder.create_stores()
    seeder.create_pricelists()
    seeder.create_pricelist_assignments()
    seeder.create_categories()
    seeder.create_products()
    seeder.create_products_inventories()
    seeder.create_prices()

    seeder.clear_token()
