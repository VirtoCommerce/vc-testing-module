from pydantic import BaseModel


class OpusCartEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_cart_type import OpusCartType

        self.cursor: str
        self.node: OpusCartType | None
