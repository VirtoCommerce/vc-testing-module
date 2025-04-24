from pydantic import BaseModel


class RemoveQuoteItemCommandType(BaseModel):
    def __init__(self):

        self.quoteId: str
        self.lineItemId: str
