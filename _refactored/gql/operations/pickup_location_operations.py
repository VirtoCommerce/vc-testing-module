from gql.types.pickup_location import PickupLocation
from gql.types.product_pickup_location import ProductPickupLocation

from .base_operations import BaseOperations, gql


class PickupLocationOperations(BaseOperations):
    def get_pickup_locations(
        self,
        store_id: str | None = None,
        keyword: str | None = None,
        sort: str | None = None,
        first: int | None = None,
        after: str | None = None,
    ) -> list[PickupLocation]:
        # fmt: off
        query = gql("""
            query PickupLocations(
                $storeId: String,
                $keyword: String,
                $sort: String,
                $first: Int,
                $after: String,
            ) {
              pickupLocations(
                storeId: $storeId,
                keyword: $keyword,
                sort: $sort,
                first: $first,
                after: $after,
              ) {
                items {
                  ...PickupLocationFragment
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "storeId": store_id,
                "keyword": keyword,
                "sort": sort,
                "first": first,
                "after": after,
            },
        )
        return [
            PickupLocation.model_validate(item)
            for item in result["data"]["pickupLocations"]["items"]
        ]

    def get_product_pickup_locations(
        self,
        product_id: str,
        store_id: str,
        culture_name: str,
        keyword: str | None = None,
        sort: str | None = None,
        first: int | None = None,
        after: str | None = None,
    ) -> list[ProductPickupLocation]:
        # fmt: off
        query = gql("""
            query ProductPickupLocations(
                $productId: String!,
                $storeId: String!,
                $cultureName: String!,
                $keyword: String,
                $sort: String,
                $first: Int,
                $after: String,
            ) {
              productPickupLocations(
                productId: $productId,
                storeId: $storeId,
                cultureName: $cultureName,
                keyword: $keyword,
                sort: $sort,
                first: $first,
                after: $after,
              ) {
                items {
                  ...ProductPickupLocationFragment
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "productId": product_id,
                "storeId": store_id,
                "cultureName": culture_name,
                "keyword": keyword,
                "sort": sort,
                "first": first,
                "after": after,
            },
        )
        return [
            ProductPickupLocation.model_validate(item)
            for item in result["data"]["productPickupLocations"]["items"]
        ]

    def get_cart_pickup_locations(
        self,
        cart_id: str,
        store_id: str,
        culture_name: str,
        keyword: str | None = None,
        sort: str | None = None,
        first: int | None = None,
        after: str | None = None,
        facet: str | None = None,
        filter: str | None = None,
    ) -> list[ProductPickupLocation]:
        # fmt: off
        query = gql("""
            query CartPickupLocations(
                $cartId: String!,
                $storeId: String!,
                $cultureName: String!,
                $keyword: String,
                $sort: String,
                $first: Int,
                $after: String,
                $facet: String,
                $filter: String,
            ) {
              cartPickupLocations(
                cartId: $cartId,
                storeId: $storeId,
                cultureName: $cultureName,
                keyword: $keyword,
                sort: $sort,
                first: $first,
                after: $after,
                facet: $facet,
                filter: $filter,
              ) {
                items {
                  ...ProductPickupLocationFragment
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "cartId": cart_id,
                "storeId": store_id,
                "cultureName": culture_name,
                "keyword": keyword,
                "sort": sort,
                "first": first,
                "after": after,
                "facet": facet,
                "filter": filter,
            },
        )
        return [
            ProductPickupLocation.model_validate(item)
            for item in result["data"]["cartPickupLocations"]["items"]
        ]
