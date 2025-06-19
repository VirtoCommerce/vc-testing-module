import allure
import pytest
from gql import Client
from gql.transport.requests import RequestsHTTPTransport


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize GraphQL Client")
def graphql_client(config, auth):
    class GraphQLClient(Client):
        def execute(self, *args, **kwargs):
            auth_headers = auth.get_auth_headers()

            if auth_headers:
                self.transport.headers.update(auth_headers)
            else:
                self.transport.headers.pop("Authorization", None)

            return super().execute(*args, **kwargs)

    transport = RequestsHTTPTransport(
        url=f"{config['backend_base_url']}/graphql",
        headers={"Content-Type": "application/json"},
        use_json=True,
        verify=True,
    )

    return GraphQLClient(transport=transport, fetch_schema_from_transport=True)
