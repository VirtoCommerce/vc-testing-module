from pydantic import BaseModel


class CartPickupLocationConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.filter_facet import FilterFacet
        from graphql_client.types.product_pickup_location import ProductPickupLocation
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.range_facet import RangeFacet
        from graphql_client.types.product_pickup_location_edge import ProductPickupLocationEdge
        from graphql_client.types.term_facet import TermFacet

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[ProductPickupLocationEdge] | None
        self.items: list[ProductPickupLocation] | None
        self.term_facets: list[TermFacet]
        self.range_facets: list[RangeFacet]
        self.filter_facets: list[FilterFacet]
