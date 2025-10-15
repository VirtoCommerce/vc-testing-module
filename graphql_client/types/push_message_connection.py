from pydantic import BaseModel


class PushMessageConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.push_message_edge import PushMessageEdge
        from graphql_client.types.push_message_type import PushMessageType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[PushMessageEdge] | None
        self.items: list[PushMessageType] | None
