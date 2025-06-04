from pydantic import BaseModel


class ProductConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.filter_facet import FilterFacet
        from graphql_client.types.product_edge import ProductEdge
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.range_facet import RangeFacet
        from graphql_client.types.term_facet import TermFacet
        from graphql_client.types.product import Product

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[ProductEdge] | None
        self.items: list[Product] | None
        self.filter_facets: list[FilterFacet]
        self.range_facets: list[RangeFacet]
        self.term_facets: list[TermFacet]
