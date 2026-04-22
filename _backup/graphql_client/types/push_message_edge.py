from pydantic import BaseModel


class PushMessageEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.push_message_type import PushMessageType

        self.cursor: str
        self.node: PushMessageType | None
