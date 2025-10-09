from pydantic import BaseModel


class OpusQuoteEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_quote_type import OpusQuoteType

        self.cursor: str
        self.node: OpusQuoteType | None
