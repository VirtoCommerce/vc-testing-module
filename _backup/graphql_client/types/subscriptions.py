from pydantic import BaseModel


class Subscriptions(BaseModel):
    def __init__(self):
        from graphql_client.types.push_message_type import PushMessageType

        self.ping: str | None
        self.pushMessageCreated: PushMessageType
