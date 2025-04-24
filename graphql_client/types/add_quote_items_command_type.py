from pydantic import BaseModel


class AddQuoteItemsCommandType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_new_quote_item_type import InputNewQuoteItemType

        self.quoteId: str
        self.newQuoteItems: list[InputNewQuoteItemType]
