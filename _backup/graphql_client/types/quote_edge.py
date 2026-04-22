from pydantic import BaseModel


class QuoteEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.quote_type import QuoteType

        self.cursor: str
        self.node: QuoteType | None
