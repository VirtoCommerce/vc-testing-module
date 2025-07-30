import allure
from fixtures.auth_fixture import Auth
import pytest
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from typing import Dict, Any


class GraphQLClient(Client):
    def __init__(self, transport: RequestsHTTPTransport, auth: Auth):
        super().__init__(transport=transport, fetch_schema_from_transport=True)
        self.auth = auth

    def execute(self, *args, **kwargs):
        auth_headers = self.auth.get_auth_headers()

        if auth_headers:
            self.transport.headers.update(auth_headers)
        else:
            self.transport.headers.pop("Authorization", None)

        return super().execute(*args, **kwargs)


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize GraphQL Client")
def graphql_client(config: Dict[str, Any], auth: Auth) -> GraphQLClient:
    transport = RequestsHTTPTransport(
        url=f"{config['backend_base_url']}/graphql",
        headers={"Content-Type": "application/json"},
        use_json=True,
        verify=True,
    )

    return GraphQLClient(transport=transport, auth=auth)
