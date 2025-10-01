import json
import random
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from colorama import Fore, Style
from colorama import init as init_colorama
from dotenv import load_dotenv


class DatasetSeeder:
    def __init__(self, dataset: Dict[str, Any]):
        self.dataset = dataset


class DatasetGenerator:
    def __init__(self, dataset_schema: Dict[str, Any]):
        self.dataset_schema = dataset_schema
        self.dataset = {}

    def generate_id(self) -> str:
        return str(uuid.uuid4())

    def create_languages(self) -> None:
        if "languages" not in self.dataset_schema:
            raise ValueError("Languages not found in dataset schema")

        self.dataset["languages"] = []
        for language in self.dataset_schema["languages"]:
            print(f'Creating language "{language}"...', end=" ")
            self.dataset["languages"].append(language)
            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_currencies(self) -> None:
        if "currencies" not in self.dataset_schema:
            raise ValueError("Currencies not found in dataset schema")

        self.dataset["currencies"] = []
        for currency in self.dataset_schema["currencies"]:
            self.dataset["currencies"].append(
                {
                    "code": currency,
                }
            )

    def create_measures(self) -> None:
        if "measures" not in self.dataset_schema:
            raise ValueError("Measures not found in dataset schema")

        self.dataset["measures"] = []
        for measure in self.dataset_schema["measures"]:
            print(f'Creating measure "{measure["name"]}"...', end=" ")
            payload = {
                "id": self.generate_id(),
                "name": measure["name"],
                "code": measure["code"],
                "units": [],
            }
            for unit in measure["units"]:
                payload["units"].append(
                    {
                        "name": unit["name"],
                        "code": unit["code"],
                        "symbol": unit["symbol"],
                        "conversionFactor": unit["conversion_factor"],
                        "localizedName": {
                            "values": {
                                self.dataset["languages"][0]["allowedValues"][0]: unit[
                                    "name"
                                ]
                            }
                        },
                        "localizedSymbol": {
                            "values": {
                                self.dataset["languages"][0]["allowedValues"][0]: unit[
                                    "name"
                                ]
                            }
                        },
                    }
                )
            self.dataset["measures"].append(payload)
            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_fulfillment_centers(self) -> None:
        if "fulfillment_centers" not in self.dataset_schema:
            raise ValueError("Fulfillment centers not found in dataset schema")

        self.dataset["fulfillmentCenters"] = []
        for ffc in self.dataset_schema["fulfillment_centers"]:
            print(f'Creating fulfillment center "{ffc["name"]}"...', end=" ")
            self.dataset["fulfillmentCenters"].append(
                {
                    "id": self.generate_id(),
                    "name": ffc["name"],
                    "address": {
                        "addressType": "Shipping",
                        "city": ffc["address"]["city"],
                        "countryCode": ffc["address"]["country_code"],
                        "countryName": ffc["address"]["country_name"],
                        "line1": ffc["address"]["line1"],
                        "postalCode": ffc["address"]["postal_code"],
                        "regionCode": ffc["address"]["region_code"],
                        "regionName": ffc["address"]["region_name"],
                        "email": ffc["address"]["email"],
                        "phone": ffc["address"]["phone"],
                    },
                }
            )
            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_catalog(self) -> None:
        if "catalog" not in self.dataset_schema:
            raise ValueError("Catalog not found in dataset schema")

        print(
            f'Creating catalog "{self.dataset_schema["catalog"]["name"]}"...', end=" "
        )
        self.dataset["catalog"] = {
            "id": self.generate_id(),
            "name": self.dataset_schema["catalog"]["name"],
            "isVirtual": False,
            "languages": [
                {
                    "languageCode": self.dataset["languages"][0]["allowedValues"][0],
                    "isActive": True,
                    "isDefault": True,
                }
            ],
        }
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_store(self) -> None:
        if "store" not in self.dataset_schema:
            raise ValueError("Store not found in dataset schema")

        print(f'Creating store "{self.dataset_schema["store"]["name"]}"...', end=" ")
        main_fulfillment_center_id = random.choice(self.dataset["fulfillmentCenters"])[
            "id"
        ]
        self.dataset["store"] = {
            "id": self.generate_id(),
            "name": self.dataset_schema["store"]["name"],
            "catalog": self.dataset["catalog"]["id"],
            "status": self.dataset_schema["store"]["status"],
            "defaultCurrency": self.dataset_schema["store"]["currency"],
            "defaultLanguage": self.dataset_schema["store"]["language_code"],
            "currencies": [
                currency
                for currency in self.dataset["currencies"]
                if currency["code"] != self.dataset_schema["store"]["currency"]
            ],
            "languages": [
                language
                for language in self.dataset["languages"]
                if language != self.dataset_schema["store"]["language_code"]
            ],
            "mainFulfillmentCenterId": main_fulfillment_center_id,
            "additionalFulfillmentCenters": [
                ffc["id"]
                for ffc in self.dataset["fulfillmentCenters"]
                if ffc["id"] != main_fulfillment_center_id
            ],
        }
        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_pricelists(self) -> None:
        self.dataset["pricelists"] = []
        for currency in self.dataset_schema["currencies"]:
            print(f"Creating pricelist for {currency}...", end=" ")
            self.dataset["pricelists"].append(
                {
                    "id": self.generate_id(),
                    "name": f"ACME pricelist {currency}",
                    "currency": currency,
                }
            )
            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_pricelist_assignments(self) -> None:
        self.dataset["pricelistAssignments"] = []
        for pricelist in self.dataset["pricelists"]:
            print(f"Creating pricelist assignment for {pricelist['name']}...", end=" ")
            self.dataset["pricelistAssignments"].append(
                {
                    "id": self.generate_id(),
                    "catalogId": self.dataset["catalog"]["id"],
                    "pricelistId": pricelist["id"],
                    "name": f"ACME pricelist assignment {pricelist['currency']}",
                }
            )
            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_categories(
        self,
        categories: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
    ) -> None:
        if "categories" not in self.dataset_schema:
            raise ValueError("Categories not found in dataset schema")

        if not categories:
            categories = self.dataset_schema["categories"]

        self.dataset["categories"] = []
        for category in categories:
            print(f"Creating category {category['name']}...", end=" ")
            payload = {
                "id": self.generate_id(),
                "code": category["name"].replace(" ", "-").lower(),
                "name": category["name"],
                "seoObjectType": "Category",
                "catalogId": self.dataset["catalog"]["id"],
                "parentId": parent_id,
            }
            self.dataset["categories"].append(payload)
            print(Fore.GREEN + "OK" + Style.RESET_ALL)

            if "categories" in category:
                self.create_categories(category["categories"], payload["id"])


def main() -> None:
    base_dir_path = Path("dataset_generator")

    with open(base_dir_path / "dataset_template.yaml", "r", encoding="utf-8") as file:
        dataset_schema = yaml.safe_load(file)

        dataset_generator = DatasetGenerator(dataset_schema)
        dataset_generator.create_languages()
        dataset_generator.create_currencies()
        dataset_generator.create_measures()
        dataset_generator.create_fulfillment_centers()
        dataset_generator.create_catalog()
        dataset_generator.create_store()
        dataset_generator.create_pricelists()
        dataset_generator.create_pricelist_assignments()
        dataset_generator.create_categories()

        json.dump(
            dataset_generator.dataset,
            open(base_dir_path / "dataset.json", "w", encoding="utf-8"),
            indent=4,
        )


if __name__ == "__main__":
    load_dotenv(override=True)
    init_colorama(autoreset=True)
    main()


"""
import json
import os
import random
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from colorama import Fore, Style
from colorama import init as init_colorama
from dotenv import load_dotenv

from fixtures import Auth, WebAPISession


class DatasetGenerator:
    def __init__(self):
        self.base_dir_path: Path = Path("dataset_generator")
        self.specs_dir_path: Path = Path(self.base_dir_path / "specs")
        self.config: Dict[str, Any] = self.get_config()
        self.auth: Auth = Auth(self.config)
        self.webapi_client: WebAPISession = WebAPISession(self.config, self.auth)
        self.dataset: Dict[str, Any] = {}
        self.components_specs: Dict[str, Any] = {}

    def get_config(self):
        return {
            "backend_base_url": os.getenv("BACKEND_BASE_URL"),
            "frontend_base_url": os.getenv("FRONTEND_BASE_URL"),
            "store_id": os.getenv("STORE_ID"),
            "admin_username": os.getenv("ADMIN_USERNAME"),
            "admin_password": os.getenv("ADMIN_PASSWORD"),
        }

    def authenticate(self, username: str, password: str) -> None:
        self.auth.authenticate(username, password)

    def sign_out(self) -> None:
        self.auth.clear_token()

    def generate_id(self) -> str:
        return str(uuid.uuid4())

    def create_fulfillment_centers(self, ffcs: List[Dict[str, Any]]) -> None:
        if not ffcs:
            raise ValueError("No fulfillment centers found")

        self.dataset["fulfillmentCenters"] = []

        for ffc in ffcs:
            print(f'Creating fulfillment center "{ffc["name"]}"...', end=" ")

            self.dataset["fulfillmentCenters"].append(
                {
                    "id": self.generate_id(),
                    "name": ffc["name"],
                    "address": {
                        "addressType": "Shipping",
                        "city": ffc["address"]["city"],
                        "countryCode": ffc["address"]["country_code"],
                        "countryName": ffc["address"]["country_name"],
                        "line1": ffc["address"]["line1"],
                        "postalCode": ffc["address"]["postal_code"],
                        "regionCode": ffc["address"]["region_code"],
                        "regionName": ffc["address"]["region_name"],
                        "email": ffc["address"]["email"],
                        "phone": ffc["address"]["phone"],
                    },
                }
            )

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_catalog(self, catalog: Dict[str, Any]) -> None:
        if not catalog:
            raise ValueError("No catalog found")

        print(f'Creating catalog "{catalog["name"]}"...', end=" ")

        self.dataset["catalog"] = {
            "id": self.generate_id(),
            "name": catalog["name"],
            "isVirtual": catalog["is_virtual"],
        }

        self.dataset["catalog"]["languages"] = []
        for language in catalog["languages"]:
            self.dataset["catalog"]["languages"].append(
                {
                    "languageCode": language["language_code"],
                    "isActive": language["is_active"],
                    "isDefault": language["is_default"],
                }
            )

        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_store(self, store: Dict[str, Any]) -> None:
        if not store:
            raise ValueError("No store found")

        print(f'Creating store "{store["name"]}"...', end=" ")

        main_ffc_id = random.choice(self.dataset["fulfillmentCenters"])["id"]

        self.dataset["store"] = {
            "id": self.generate_id(),
            "name": store["name"],
            "currency": store["currency"],
            "languageCode": store["language_code"],
            "status": store["status"],
            "languages": store["languages"],
            "currencies": store["currencies"],
            "fulfillmentCenterId": main_ffc_id,
            "additionalFulfillmentCenters": list(
                map(
                    lambda ffc: ffc["id"],
                    [
                        ffc
                        for ffc in self.dataset["fulfillmentCenters"]
                        if ffc["id"] != main_ffc_id
                    ],
                )
            ),
        }

        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_pricelist(self, pricelist: Dict[str, Any]) -> None:
        if not pricelist:
            raise ValueError("No pricelist found")

        print(f'Creating pricelist "{pricelist["name"]}"...', end=" ")

        self.dataset["pricelist"] = {
            "id": self.generate_id(),
            "name": pricelist["name"],
            "currency": pricelist["currency"],
        }
        self.dataset["pricelistAssignment"] = {
            "catalogId": self.dataset["catalog"]["id"],
            "pricelistId": self.dataset["pricelist"]["id"],
            "name": "ACME Pricelist Assignment",
        }

        print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def update_components_specs(self, spec_filenames: List[str]) -> None:
        for spec_filename in spec_filenames:
            with open(
                self.specs_dir_path / spec_filename, "r", encoding="utf-8"
            ) as file:
                component_spec = yaml.safe_load(file)
                for components_family in component_spec:
                    for model in components_family["models"]:
                        self.components_specs[model["id"]] = model

    def create_properties(self, category_id: str, properties: Dict[str, Any]) -> None:
        self.dataset["properties"] = []
        for property in properties:
            print(f'Creating property "{property["name"]}"...', end=" ")
            property = {
                "id": self.generate_id(),
                "catalogId": self.dataset["catalog"]["id"],
                "categoryId": category_id,
                "name": property["name"],
                "displayNames": [
                    {
                        "name": property["display_name"],
                        "languageCode": self.dataset["store"]["languageCode"],
                    }
                ],
                "type": property["object_type"],
                "valueType": property["type"],
            }
            if not self.dataset["properties"][property["name"]]:
                self.dataset["properties"].append(property)
            else:
                self.dataset["properties"][property["name"]] = property
            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def process_category_specs(self, category: Dict[str, Any]) -> None:
        print(
            f'Processing specs for category "{category["name"]}"...',
            end=" ",
        )

        category_specs_file = Path(self.specs_dir_path / category["specs"])
        if not category_specs_file.exists():
            print(Fore.YELLOW + f"NOT FOUND: {category_specs_file}" + Style.RESET_ALL)
            return

        with open(
            self.specs_dir_path / category["specs"], "r", encoding="utf-8"
        ) as file:
            category_specs = yaml.safe_load(file)
            for category_spec in category_specs:
                if "components_specs" in category_spec:
                    self.update_components_specs(category_spec["components_specs"])
                if "properties" in category_spec:
                    self.create_properties(category_spec["properties"])

    def create_categories(
        self, categories: Dict[str, Any], parent_id: Optional[str] = None
    ) -> None:
        if not categories:
            raise ValueError("No categories found")

        if not parent_id:
            self.dataset["categories"] = []

        for yaml_category in categories:
            print(f'Creating categories "{yaml_category["name"]}"...', end=" ")

            category = {
                "id": self.generate_id(),
                "code": yaml_category["name"].replace(" ", "-").lower(),
                "name": yaml_category["name"],
                "seoObjectType": "Category",
                "catalogId": self.dataset["catalog"]["id"],
            }

            if parent_id:
                category["parentId"] = parent_id

            self.dataset["categories"].append(category)

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

            if "specs" in yaml_category:
                self.process_category_specs(yaml_category)

            if "categories" in yaml_category and len(yaml_category["categories"]) > 0:
                self.create_categories(yaml_category["categories"], category["id"])


def main() -> None:
    dataset_generator = DatasetGenerator()

    with open(
        dataset_generator.base_dir_path / "dataset_template.yaml", "r", encoding="utf-8"
    ) as file:
        dataset = yaml.safe_load(file)
        dataset_generator.create_fulfillment_centers(dataset["fulfillment_centers"])
        dataset_generator.create_catalog(dataset["catalog"])
        dataset_generator.create_store(dataset["store"])
        dataset_generator.create_pricelist(dataset["pricelist"])
        dataset_generator.create_categories(dataset["catalog"]["categories"])

        json.dump(
            dataset_generator.dataset,
            open(dataset_generator.base_dir_path / "dataset.json", "w"),
            indent=4,
        )


if __name__ == "__main__":
    load_dotenv(override=True)
    init_colorama(autoreset=True)
    main()
"""
