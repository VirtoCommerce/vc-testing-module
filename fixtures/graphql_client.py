import allure
import pytest
from gql import Client
from gql.transport.requests import RequestsHTTPTransport


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize GraphQL Client")
def graphql_client(config):
    headers = {}

    def set_headers(headers_object: dict):
        nonlocal headers

        headers.update(headers_object)

    transport = RequestsHTTPTransport(
        url=f"{config['base_url']}/graphql",
        headers=headers,
        use_json=True,
        verify=True,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)
    client.set_headers = set_headers

    return client
