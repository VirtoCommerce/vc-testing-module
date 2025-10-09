from pydantic import BaseModel


class OpusContactEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_contact_type import OpusContactType

        self.cursor: str
        self.node: OpusContactType | None
