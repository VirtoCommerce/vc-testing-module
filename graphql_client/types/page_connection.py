from pydantic import BaseModel


class PageConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_type import PageType
        from graphql_client.types.page_edge import PageEdge
        from graphql_client.types.page_info import PageInfo

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[PageEdge] | None
        self.items: list[PageType] | None
