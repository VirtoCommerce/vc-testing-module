import allure
import pytest
from gql import Client
from gql.transport.requests import RequestsHTTPTransport


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize GraphQL Client")
def graphql_client(config, auth_token):
    transport = RequestsHTTPTransport(
        url=f"{config['base_url']}/graphql",
        headers={
            "Authorization": f"Bearer {auth_token[0]}",
        },
        use_json=True,
        verify=True,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client
