from pydantic import BaseModel


class CreateQuoteRequestsResultType(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_quote_type import OpusQuoteType

        self.quotes: list[OpusQuoteType] | None
