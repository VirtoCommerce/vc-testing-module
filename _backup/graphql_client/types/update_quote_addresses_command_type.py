from pydantic import BaseModel


class UpdateQuoteAddressesCommandType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_quote_address_type import InputQuoteAddressType

        self.quoteId: str
        self.addresses: list[InputQuoteAddressType]
