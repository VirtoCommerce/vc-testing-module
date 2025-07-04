from pydantic import BaseModel


class QuoteConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.quote_type import QuoteType
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.quote_edge import QuoteEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[QuoteEdge] | None
        self.items: list[QuoteType] | None
