from pydantic import BaseModel


class OpusCartConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.opus_cart_type import OpusCartType
        from graphql_client.types.opus_cart_edge import OpusCartEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[OpusCartEdge] | None
        self.items: list[OpusCartType] | None
