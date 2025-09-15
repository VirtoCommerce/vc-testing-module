import json
import os
from typing import Any, Dict

from colorama import Fore, Style
from colorama import init as init_colorama
from dotenv import load_dotenv

from fixtures import Auth, WebAPISession


class DatasetSeeder:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.auth = Auth(config)
        self.webapi_client = WebAPISession(config, self.auth)
        self.test_data = None
        self.store_id = None

    def get_file_path(self, file_name: str) -> str:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file_name)

        return file_path

    def authenticate(self, username: str, password: str) -> None:
        self.auth.authenticate(username, password)

    def sign_out(self) -> None:
        self.auth.clear_token()

    def load_test_data(self, file_path: str) -> None:
        with open(self.get_file_path(file_path), "r") as file:
            self.test_data = json.load(file)

    def load_test_data_users(self, file_path: str) -> None:
        with open(self.get_file_path(file_path), "r") as file:
            self.test_data_users = json.load(file)

    def create_languages(self) -> None:
        if not self.test_data["languages"]:
            raise ValueError("No languages found in test data")

        for language in self.test_data["languages"]:
            print(f'Creating language "{language}"...', end=" ")

            default_culture = self.test_data["languages"][0]

            self.webapi_client.post(
                "/api/platform/settings",
                data=[
                    {
                        "allowedValues": self.test_data["languages"],
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
        if not self.test_data["currencies"]:
            raise ValueError("No currencies found in test data")

        for currency in self.test_data["currencies"]:
            print(f'Creating currency "{currency["code"]}"...', end=" ")

            self.webapi_client.post(
                "/api/currencies",
                data=currency,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_measures(self) -> None:
        if not self.test_data["measures"]:
            raise ValueError("No measures found in test data")

        for measure in self.test_data["measures"]:
            print(f'Creating measure "{measure["name"]}"...', end=" ")
            self.webapi_client.put(
                "/api/catalog/measures",
                data=measure,
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

    def create_property_groups(self) -> None:
        if not self.test_data["propertyGroups"]:
            raise ValueError("No property groups found in test data")

        for property_group in self.test_data["propertyGroups"]:
            print(f'Creating property group "{property_group["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/catalog/propertygroups",
                data=property_group,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_properties(self) -> None:
        if not self.test_data["properties"]:
            raise ValueError("No properties found in test data")

        for property in self.test_data["properties"]:
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
        if not self.test_data["stores"]:
            raise ValueError("No stores found in test data")

        for store in self.test_data["stores"]:
            print(f'Creating store "{store["name"]}"...', end=" ")

            store["url"] = f"{self.config['frontend_base_url']}"
            self.store_id = store["id"]

            self.webapi_client.post(
                "/api/stores",
                data=store,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_aggregation_properties(self) -> None:
        if not self.test_data["aggregationProperties"]:
            raise ValueError("No aggregation properties found in test data")

        if not self.store_id:
            raise ValueError("Store ID not found")

        print(f"Creating aggregation properties...", end=" ")

        self.webapi_client.put(
            f"/api/catalog/aggregationproperties/{self.store_id}/properties",
            data=self.test_data["aggregationProperties"],
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

    def create_roles(self) -> None:
        if not self.test_data["roles"]:
            raise ValueError("No roles found in test data")

        for role in self.test_data["roles"]:
            print(f'Creating role "{role["name"]}"...', end=" ")

            self.webapi_client.put(
                "/api/platform/security/roles",
                data=role,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_organizations(self) -> None:
        if not self.test_data["organizations"]:
            raise ValueError("No organizations found in test data")

        for organization in self.test_data["organizations"]:
            print(f'Creating organization "{organization["name"]}"...', end=" ")

            self.webapi_client.post(
                "/api/members",
                data=organization,
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_contacts(self) -> None:
        if not self.test_data["contacts"]:
            raise ValueError("No contacts found in test data")

        for contact in self.test_data["contacts"]:
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
        if not self.test_data["users"]:
            raise ValueError("No users found in test data")

        for user in self.test_data["users"]:
            print(f'Creating user "{user["userName"]}"...', end=" ")

            user["password"] = self.config["users_password"]
            self.webapi_client.post(
                "/api/platform/security/users/create",
                data=user,
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
        "users_password": os.getenv("USERS_PASSWORD"),
    }


if __name__ == "__main__":
    init_colorama()

    config = get_config()

    seeder = DatasetSeeder(config)
    seeder.authenticate(config["admin_username"], config["admin_password"])

    seeder.load_test_data("dataset.json")
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
    seeder.create_roles()
    seeder.create_organizations()
    seeder.create_contacts()
    seeder.create_users()

    seeder.sign_out()
