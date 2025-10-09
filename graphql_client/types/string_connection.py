from pydantic import BaseModel


class StringConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.string_edge import StringEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[StringEdge] | None
        self.items: list[str] | None
