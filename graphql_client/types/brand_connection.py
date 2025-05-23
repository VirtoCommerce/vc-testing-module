from pydantic import BaseModel


class BrandConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.brand_edge import BrandEdge
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.brand_type import BrandType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[BrandEdge] | None
        self.items: list[BrandType] | None
