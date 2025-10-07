from pydantic import BaseModel


class CustomerOrderConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.customer_order_edge import CustomerOrderEdge
        from graphql_client.types.filter_facet import FilterFacet
        from graphql_client.types.customer_order_type import CustomerOrderType
        from graphql_client.types.term_facet import TermFacet
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.range_facet import RangeFacet

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[CustomerOrderEdge] | None
        self.items: list[CustomerOrderType] | None
        self.term_facets: list[TermFacet]
        self.range_facets: list[RangeFacet]
        self.filter_facets: list[FilterFacet]
