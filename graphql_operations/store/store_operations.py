from typing import Optional
from gql import Client
from graphql_client.types.store_response_type import StoreResponseType
from graphql_client.queries.store import StoreQuery
from graphql_operations.store.fragments.store_fragment import STORE_FRAGMENT


class StoreOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_store(
        self, store_id: Optional[str] = None, culture_name: Optional[str] = None, domain: Optional[str] = None
    ) -> StoreResponseType:
        store_query = StoreQuery(self.graphql_client)

        variables = {"storeId": store_id, "cultureName": culture_name, "domain": domain}

        result = store_query.execute(variables=variables, return_fields=STORE_FRAGMENT)

        return result
