from pydantic import BaseModel


class OpusQuoteConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_quote_type import OpusQuoteType
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.opus_quote_edge import OpusQuoteEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[OpusQuoteEdge] | None
        self.items: list[OpusQuoteType] | None
