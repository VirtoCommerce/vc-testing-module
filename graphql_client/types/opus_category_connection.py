from pydantic import BaseModel


class OpusCategoryConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.category import Category
        from graphql_client.types.opus_category_edge import OpusCategoryEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[OpusCategoryEdge] | None
        self.items: list[Category] | None
