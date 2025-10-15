from pydantic import BaseModel


class PropertyConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.property import Property
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.property_edge import PropertyEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[PropertyEdge] | None
        self.items: list[Property] | None
