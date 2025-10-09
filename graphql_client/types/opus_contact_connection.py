from pydantic import BaseModel


class OpusContactConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_contact_edge import OpusContactEdge
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.opus_contact_type import OpusContactType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[OpusContactEdge] | None
        self.items: list[OpusContactType] | None
