from pydantic import BaseModel


class ProductPickupLocationConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.product_pickup_location_edge import ProductPickupLocationEdge
        from graphql_client.types.product_pickup_location import ProductPickupLocation

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[ProductPickupLocationEdge] | None
        self.items: list[ProductPickupLocation] | None
