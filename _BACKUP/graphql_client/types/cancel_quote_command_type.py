from pydantic import BaseModel


class CancelQuoteCommandType(BaseModel):
    def __init__(self):

        self.quoteId: str
        self.comment: str
