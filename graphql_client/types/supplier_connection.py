from pydantic import BaseModel


class SupplierConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.range_facet import RangeFacet
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.term_facet import TermFacet
        from graphql_client.types.supplier_type import SupplierType
        from graphql_client.types.filter_facet import FilterFacet
        from graphql_client.types.supplier_edge import SupplierEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[SupplierEdge] | None
        self.items: list[SupplierType] | None
        self.filter_facets: list[FilterFacet]
        self.range_facets: list[RangeFacet]
        self.term_facets: list[TermFacet]
