import json
import os
from typing import Any, Literal
from urllib.parse import urlencode

from colorama import Fore, Style
from colorama import init as init_colorama
from dotenv import load_dotenv
from rich.progress import track

from dataset.dataset_config import DatasetConfig


class DatasetSeeder(DatasetConfig):
    def __init__(self):
        super().__init__()
        self.dataset = None
        self.errors = []

    def _send_request(
        self,
        method: Literal["get", "post", "put", "delete"],
        endpoint: str,
        payload: dict,
        label: str = "",
        query: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        print(f"{label}... ", end=" ")

        if query:
            query_string = urlencode(query)
            endpoint = f"{endpoint}?{query_string}"

        try:
            self.webapi_client.request(
                method=method,
                endpoint=endpoint,
                data=payload,
                **kwargs,
            )
            print(Fore.GREEN + "OK" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "ERROR" + Style.RESET_ALL)
            self.errors.append(e)

    def update_payment_methods(self) -> None:
        print("\nUpdating payment methods")

        for payment_method in self.available_payment_methods:
            payment_method["storeId"] = self.store_id
            payment_method["isActive"] = True
            self._send_request(
                label=f"-- Updating {payment_method['name']}",
                method="PUT",
                endpoint="/api/payment",
                payload=payment_method,
            )

    def update_shipping_methods(self) -> None:
        print("\nUpdating shipping methods")

        for shipping_method in self.available_shipping_methods:
            shipping_method["storeId"] = self.store_id
            shipping_method["isActive"] = True

            if shipping_method["code"] == "FixedRate":
                shipping_method["settings"] = [
                    {
                        "groupName": "General",
                        "objectId": shipping_method["id"],
                        "objectType": "FixedRateShippingMethod",
                        "name": "VirtoCommerce.Shipping.FixedRateShippingMethod.Ground.Rate",
                        "value": 20.00,
                        "valueType": "Decimal",
                    },
                    {
                        "groupName": "General",
                        "objectId": shipping_method["id"],
                        "objectType": "FixedRateShippingMethod",
                        "name": "VirtoCommerce.Shipping.FixedRateShippingMethod.Air.Rate",
                        "value": 35.00,
                        "valueType": "Decimal",
                    },
                ]

            self._send_request(
                label=f"-- Updating {shipping_method['name']}",
                method="PUT",
                endpoint="/api/shipping",
                payload=shipping_method,
            )

    def fetch_dataset(self) -> None:
        print("\nFetching dataset from JSON")

        with open(self.base_dir / "data/_index.json", "r", encoding="utf-8") as file:
            index_file: dict[str, dict] = json.load(file)
            self.dataset = {}

        for key, value in index_file.items():
            print(f"-- Fetching dataset {key}...", end=" ")
            payload = value.get("payload")
            if not payload:
                print(Fore.YELLOW + "WARNING: No payload found" + Style.RESET_ALL)
                continue
            elif not value.get("method"):
                print(Fore.YELLOW + "WARNING: No method found" + Style.RESET_ALL)
                continue
            elif not value.get("endpoint"):
                print(Fore.YELLOW + "WARNING: No endpoint found" + Style.RESET_ALL)
                continue

            self.dataset[key] = value

            with open(self.base_dir / "data" / payload, "r", encoding="utf-8") as file:
                self.dataset[key]["payload"] = json.load(file)

            with open(self.base_dir / "dataset.json", "w", encoding="utf-8") as file:
                payloads = {
                    key: section["payload"]
                    for key, section in self.dataset.items()
                    if "payload" in section
                }

                json.dump(payloads, file, indent=4)

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def seed(self) -> None:
        print(f"\nSeeding dataset to {self.config['backend_base_url']}")

        for key, value in self.dataset.items():
            items_per_request = value["itemsPerRequest"]
            method = value["method"]
            endpoint_template = str(value["endpoint"])

            items = (
                value["payload"]
                if items_per_request == "single"
                else [value["payload"]]
            )

            for item in items:
                endpoint = endpoint_template
                if "id" in item:
                    endpoint = endpoint_template.format(id=item["id"])
                if "{storeId}" in endpoint:
                    endpoint = endpoint_template.format(storeId=self.store_id)
                if "{productId}" in endpoint:
                    endpoint = endpoint_template.format(productId=item["productId"])
                if "url" in item and "{storeUrl}" in item["url"]:
                    item["url"] = self.config["frontend_base_url"]

                label = f"-- Seeding {key}"
                if "name" in item:
                    label += f": {item['name']}"
                elif "code" in item:
                    label += f": {item['code']}"
                elif "id" in item:
                    label += f": {item['id']}"
                label += f" {Fore.LIGHTBLACK_EX}[{method}: {endpoint}]{Style.RESET_ALL}"

                if key == "users":
                    item["password"] = self.config["users_password"]

                self._send_request(
                    label=label,
                    method=method,
                    endpoint=endpoint,
                    payload=item,
                )


if __name__ == "__main__":
    init_colorama()

    seeder = DatasetSeeder()
    seeder.authenticate(
        seeder.config["admin_username"], seeder.config["admin_password"]
    )

    seeder.get_available_shipping_methods()
    seeder.get_available_payment_methods()
    seeder.fetch_dataset()

    seeder.seed()
    seeder.update_payment_methods()
    seeder.update_shipping_methods()

    if seeder.errors:
        print(os.linesep)
        print(Fore.RED + "ERRORS" + Style.RESET_ALL)
        for error in seeder.errors:
            print("===================================================================")
            print(error.message)

    seeder.sign_out()
