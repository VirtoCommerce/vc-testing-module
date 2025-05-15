from gql import Client
from graphql_client.types.product_connection import ProductConnection
from graphql_client.types.product import Product
from graphql_client.queries.products import ProductsQuery
from graphql_client.queries.product import ProductQuery
from tests_graphql.operations.catalog.fragments.product_fragment import PRODUCT_FRAGMENT
from graphql_client.types.configuration_line_item_type import ConfigurationLineItemType
from graphql_client.types.input_create_configured_line_item_command import InputCreateConfiguredLineItemCommand
from graphql_client.mutations.create_configured_line_item import CreateConfiguredLineItemMutation
from tests_graphql.operations.catalog.fragments.configuration_line_item_fragment import CONFIGURATION_LINE_ITEM_FRAGMENT
from graphql_client.queries.product_configuration import ProductConfigurationQuery
from graphql_client.types.configuration_query_response_type import ConfigurationQueryResponseType
from tests_graphql.operations.catalog.fragments.configuration_section_fragment import CONFIGURATION_SECTION_FRAGMENT


class ProductsOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_products(
        self, store_id: str, user_id: str, currency_code: str, culture_name: str, query: str = None, filter: str = None
    ) -> ProductConnection:
        products_query = ProductsQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "userId": user_id,
            "currencyCode": currency_code,
            "cultureName": culture_name,
            "query": query,
            "filter": filter,
        }

        return_fields = f"""
            totalCount
            items {{
                {PRODUCT_FRAGMENT}
            }}
        """

        result = products_query.execute(variables=variables, return_fields=return_fields)

        return result

    def get_product(self, store_id: str, user_id: str, culture_name: str, currency_code: str, id: str) -> Product:
        product_query = ProductQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "userId": user_id,
            "cultureName": culture_name,
            "currencyCode": currency_code,
            "id": id,
        }

        result = product_query.execute(variables=variables, return_fields=PRODUCT_FRAGMENT)

        return result

    def get_product_configuration(
        self,
        store_id: str,
        user_id: str,
        configurable_product_id: str,
        culture_name: str,
        currency_code: str,
    ) -> ConfigurationQueryResponseType:
        product_configuration_query = ProductConfigurationQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "userId": user_id,
            "configurableProductId": configurable_product_id,
            "cultureName": culture_name,
            "currencyCode": currency_code,
        }

        return_fields = f"""
            configurationSections {{
                {CONFIGURATION_SECTION_FRAGMENT}
            }}
        """

        result = product_configuration_query.execute(variables=variables, return_fields=return_fields)

        return result

    def create_configured_line_item(self, payload: InputCreateConfiguredLineItemCommand) -> ConfigurationLineItemType:
        create_configured_line_item_mutation = CreateConfiguredLineItemMutation(self.graphql_client)

        variables = {"command": payload}

        result = create_configured_line_item_mutation.execute(
            variables=variables, return_fields=CONFIGURATION_LINE_ITEM_FRAGMENT
        )

        return result
