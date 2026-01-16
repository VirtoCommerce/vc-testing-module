from gql import Client

from graphql_client.queries.pickup_locations import PickupLocationsQuery
from graphql_client.queries.product_pickup_locations import ProductPickupLocationsQuery
from graphql_client.queries.cart_pickup_locations import CartPickupLocationsQuery
from graphql_client.types.pickup_location_connection import PickupLocationConnection
from graphql_client.types.product_pickup_location_connection import ProductPickupLocationConnection
from graphql_client.types.cart_pickup_location_connection import CartPickupLocationConnection
from graphql_operations.pickup_locations.fragments.pickup_locations_fragment import PICKUP_LOCATION_FRAGMENT
from graphql_operations.pickup_locations.fragments.product_pickup_locations_fragment import PRODUCT_PICKUP_LOCATION_FRAGMENT
from graphql_operations.pickup_locations.fragments.cart_pickup_locations_fragment import CART_PICKUP_LOCATION_FRAGMENT


class PickupLocationsOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_pickup_locations(
        self,
        store_id: str,
        first: int = None,
        after: str = None,
        keyword: str = None,
        sort: str = None,
    ) -> PickupLocationConnection:
        """Get all pickup locations for a store"""
        pickup_locations_query = PickupLocationsQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "first": first,
            "after": after,
            "keyword": keyword,
            "sort": sort,
        }

        variables = {k: v for k, v in variables.items() if v is not None}

        result = pickup_locations_query.execute(
            variables=variables, return_fields=PICKUP_LOCATION_FRAGMENT
        )

        return result

    def get_product_pickup_locations(
        self,
        product_id: str,
        store_id: str,
        culture_name: str,
        first: int = None,
        after: str = None,
        keyword: str = None,
        sort: str = None,
    ) -> ProductPickupLocationConnection:
        """Get pickup locations available for a specific product"""
        product_pickup_locations_query = ProductPickupLocationsQuery(self.graphql_client)

        variables = {
            "productId": product_id,
            "storeId": store_id,
            "cultureName": culture_name,
            "first": first,
            "after": after,
            "keyword": keyword,
            "sort": sort,
        }

        variables = {
            k: v
            for k, v in variables.items()
            if v is not None or k in ["productId", "storeId", "cultureName"]
        }

        result = product_pickup_locations_query.execute(
            variables=variables, return_fields=PRODUCT_PICKUP_LOCATION_FRAGMENT
        )

        return result

    def get_cart_pickup_locations(
        self,
        cart_id: str,
        store_id: str,
        culture_name: str,
        first: int = None,
        after: str = None,
        keyword: str = None,
        sort: str = None,
        facet: str = None,
        filter: str = None,
    ) -> CartPickupLocationConnection:
        """Get pickup locations available for items in a cart"""
        cart_pickup_locations_query = CartPickupLocationsQuery(self.graphql_client)

        variables = {
            "cartId": cart_id,
            "storeId": store_id,
            "cultureName": culture_name,
            "first": first,
            "after": after,
            "keyword": keyword,
            "sort": sort,
            "facet": facet,
            "filter": filter,
        }
      
        variables = {
            k: v
            for k, v in variables.items()
            if v is not None or k in ["cartId", "storeId", "cultureName"]
        }

        result = cart_pickup_locations_query.execute(
            variables=variables, return_fields=CART_PICKUP_LOCATION_FRAGMENT
        )

        return result

