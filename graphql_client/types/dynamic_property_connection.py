from pydantic import BaseModel


class DynamicPropertyConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.dynamic_property_edge import DynamicPropertyEdge
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.dynamic_property_type import DynamicPropertyType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[DynamicPropertyEdge] | None
        self.items: list[DynamicPropertyType] | None
