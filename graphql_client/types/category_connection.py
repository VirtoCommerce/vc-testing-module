from pydantic import BaseModel


class CategoryConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.category import Category
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.category_edge import CategoryEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[CategoryEdge] | None
        self.items: list[Category] | None
