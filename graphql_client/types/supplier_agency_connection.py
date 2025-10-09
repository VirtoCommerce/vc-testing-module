from pydantic import BaseModel


class SupplierAgencyConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.supplier_agency_type import SupplierAgencyType
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.supplier_agency_edge import SupplierAgencyEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[SupplierAgencyEdge] | None
        self.items: list[SupplierAgencyType] | None
