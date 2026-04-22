from gql.types.configuration_line_item import ConfigurationLineItem
from gql.types.configuration_section_input import ConfigurationSectionInput
from gql.types.product import Product
from gql.types.product_configuration import ProductConfiguration

from .base_operations import BaseOperations, gql


class ProductOperations(BaseOperations):
    def get_products(
        self,
        store_id: str,
        user_id: str | None = None,
        culture_name: str | None = None,
        currency_code: str | None = None,
        query: str | None = None,
        filter: str | None = None,
        sort: str | None = None,
        first: int | None = None,
        after: str | None = None,
    ) -> list[Product]:
        # fmt: off
        gql_query = gql("""
            query Products(
                $storeId: String!,
                $userId: String,
                $cultureName: String,
                $currencyCode: String,
                $query: String,
                $filter: String,
                $sort: String,
                $first: Int,
                $after: String,
            ) {
              products(
                storeId: $storeId,
                userId: $userId,
                cultureName: $cultureName,
                currencyCode: $currencyCode,
                query: $query,
                filter: $filter,
                sort: $sort,
                first: $first,
                after: $after,
              ) {
                items {
                  ...ProductFragment
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(gql_query),
            variables={
                "storeId": store_id,
                "userId": user_id,
                "cultureName": culture_name,
                "currencyCode": currency_code,
                "query": query,
                "filter": filter,
                "sort": sort,
                "first": first,
                "after": after,
            },
        )
        return [Product.model_validate(item) for item in result["data"]["products"]["items"]]

    def get_product_configuration(
        self,
        configurable_product_id: str,
        store_id: str,
        user_id: str | None = None,
        culture_name: str | None = None,
        currency_code: str | None = None,
    ) -> ProductConfiguration | None:
        # fmt: off
        gql_query = gql("""
            query ProductConfiguration(
                $configurableProductId: String!,
                $storeId: String!,
                $userId: String,
                $cultureName: String,
                $currencyCode: String,
            ) {
              productConfiguration(
                configurableProductId: $configurableProductId,
                storeId: $storeId,
                userId: $userId,
                cultureName: $cultureName,
                currencyCode: $currencyCode,
              ) {
                ...ProductConfigurationFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(gql_query),
            variables={
                "configurableProductId": configurable_product_id,
                "storeId": store_id,
                "userId": user_id,
                "cultureName": culture_name,
                "currencyCode": currency_code,
            },
        )
        data = result["data"]["productConfiguration"]
        return ProductConfiguration.model_validate(data) if data else None

    def create_configured_line_item(
        self,
        configurable_product_id: str,
        configuration_sections: list[ConfigurationSectionInput],
        store_id: str | None = None,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> ConfigurationLineItem:
        # fmt: off
        mutation = gql("""
            mutation CreateConfiguredLineItem($command: InputCreateConfiguredLineItemCommand!) {
              createConfiguredLineItem(command: $command) {
                ...ConfigurationLineItemFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "configurableProductId": configurable_product_id,
                    "configurationSections": [
                        s.model_dump(by_alias=True, exclude_none=True) for s in configuration_sections
                    ],
                    **({"storeId": store_id} if store_id else {}),
                    **({"currencyCode": currency_code} if currency_code else {}),
                    **({"cultureName": culture_name} if culture_name else {}),
                }
            },
        )
        return ConfigurationLineItem.model_validate(result["data"]["createConfiguredLineItem"])
