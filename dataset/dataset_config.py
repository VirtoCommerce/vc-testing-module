import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from gql.transport.requests import RequestsHTTPTransport

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from fixtures.webapi_client import WebAPISession


class DatasetConfig:
    def __init__(self):
        load_dotenv(override=True)
        self.base_dir = Path(__file__).parent
        self.config = {
            "backend_base_url": os.getenv("BACKEND_BASE_URL"),
            "frontend_base_url": os.getenv("FRONTEND_BASE_URL"),
            "store_id": os.getenv("STORE_ID"),
            "admin_username": os.getenv("ADMIN_USERNAME"),
            "admin_password": os.getenv("ADMIN_PASSWORD"),
            "users_password": os.getenv("USERS_PASSWORD"),
        }
        self.transport = RequestsHTTPTransport(
            url=f"{self.config['backend_base_url']}/graphql",
            headers={"Content-Type": "application/json"},
            use_json=True,
            verify=True,
        )
        self.auth = Auth(self.config)
        self.graphql_client = GraphQLClient(self.transport, self.auth)
        self.webapi_client = WebAPISession(self.config, self.auth)
        self.store_id = self.config["store_id"]
        self.language = self.get_json(self.base_dir / "data" / "languages.json")[0][
            "defaultValue"
        ]
        self.currencies = self.get_json(self.base_dir / "data" / "currencies.json")
        self.products = self.get_json(self.base_dir / "data" / "products.json")
        self.users = self.get_json(self.base_dir / "data" / "users.json")
        self.organizations = self.get_json(
            self.base_dir / "data" / "organizations.json"
        )
        self.pickup_locations = self.get_json(
            self.base_dir / "data" / "pickup_locations.json"
        )

    config: dict[str, Any]
    base_dir: Path
    transport: RequestsHTTPTransport
    auth: Auth
    graphql_client: GraphQLClient
    webapi_client: WebAPISession
    store_id: str
    language: str
    currencies: list[dict[str, Any]]
    products: list[dict[str, Any]]
    users: list[dict[str, Any]]
    organizations: list[dict[str, Any]]
    pickup_locations: list[dict[str, Any]]
    available_shipping_methods: list[dict[str, Any]]
    available_payment_methods: list[dict[str, Any]]

    def authenticate(self, username: str, password: str) -> None:
        self.auth.authenticate(username, password)

    def sign_out(self) -> None:
        self.auth.clear_token()

    def get_json(self, file_path: Path) -> dict[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON file {file_path}: {e}")
            print(
                "To successfully run the script, you need to have the following files in the data folder:"
            )
            print("- languages.json")
            print("- currencies.json")
            print("- products.json")
            print("- users.json")
            print("- organizations.json")
            print("- pickup_locations.json")
            raise e

    def get_available_shipping_methods(self) -> None:
        self.available_shipping_methods = self.webapi_client.post(
            "/api/shipping/search", data={"storeId": self.store_id}
        )["results"]

    def get_available_payment_methods(self) -> None:
        self.available_payment_methods = self.webapi_client.post(
            "/api/payment/search", data={"storeId": self.store_id}
        )["results"]
