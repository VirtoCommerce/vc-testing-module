import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlencode

from colorama import Fore, Style
from colorama import init as init_colorama
from dotenv import load_dotenv
from gql.transport.requests import RequestsHTTPTransport

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from fixtures.webapi_client import WebAPISession


class DatasetSeeder:
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.base_dir = Path(__file__).parent
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
        self.errors = []
        self.store_id = config["store_id"]

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

        payment_methods = self.webapi_client.post(
            "/api/payment/search", data={"storeId": self.store_id}
        )["results"]

        for payment_method in payment_methods:
            payment_method["isActive"] = True
            self._send_request(
                label=f"-- Updating {payment_method['name']}",
                method="PUT",
                endpoint="/api/payment",
                payload=payment_method,
            )

    def update_shipping_methods(self) -> None:
        print("\nUpdating shipping methods")

        shipping_methods = self.webapi_client.post(
            "/api/shipping/search", data={"storeId": self.store_id}
        )["results"]

        for shipping_method in shipping_methods:
            shipping_method["isActive"] = True
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

    def authenticate(self, username: str, password: str) -> None:
        self.auth.authenticate(username, password)

    def sign_out(self) -> None:
        self.auth.clear_token()

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

            if key == "users":
                users_password = self.config["users_password"]

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

    def create_users(self) -> None:
        if not self.dataset["users"]:
            raise ValueError("No users found in dataset")

        for user in self.dataset["users"]:
            print(f'Creating user "{user["userName"]}"...', end=" ")

            user["password"] = self.config["users_password"]

            try:
                self.webapi_client.post(
                    "/api/platform/security/users/create",
                    data=user,
                )
            except Exception as e:
                return

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def create_notifications(self) -> None:
        if not self.dataset["notifications"]:
            raise ValueError("No notifications found in dataset")

        for notification in self.dataset["notifications"]:
            print(f'Creating notification "{notification["alias"]}"...', end=" ")
            try:
                self.webapi_client.post(
                    "api/notifications/RegistrationInvitationEmailNotification",
                    data=notification,
                )
            except Exception as e:
                return

            print(Fore.GREEN + "OK" + Style.RESET_ALL)

    def generate_orders(self, count: int = 1) -> None:
        orders = []
        for i in range(count):
            order_id_part = f"{datetime.today().strftime("%d%m%Y")}-{i + 1}"
            orders.append(
                {
                    "id": f"order-acme-{order_id_part}",
                    "number": f"CO-{order_id_part}",
                    "status": random.choice(
                        ["New", "Completed", "Cancelled", "Pending", "Processing"]
                    ),
                }
            )

        with open(
            self.base_dir / "data" / "orders.json", "w", encoding="utf-8"
        ) as file:
            json.dump(orders, file, indent=4)


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
    # seeder.generate_orders(1)
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
