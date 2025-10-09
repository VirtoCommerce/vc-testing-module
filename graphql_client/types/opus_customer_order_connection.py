from pydantic import BaseModel


class OpusCustomerOrderConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_customer_order_edge import OpusCustomerOrderEdge
        from graphql_client.types.range_facet import RangeFacet
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.term_facet import TermFacet
        from graphql_client.types.filter_facet import FilterFacet
        from graphql_client.types.opus_customer_order_type import OpusCustomerOrderType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[OpusCustomerOrderEdge] | None
        self.items: list[OpusCustomerOrderType] | None
        self.term_facets: list[TermFacet]
        self.range_facets: list[RangeFacet]
        self.filter_facets: list[FilterFacet]
