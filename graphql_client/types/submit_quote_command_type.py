from pydantic import BaseModel


class SubmitQuoteCommandType(BaseModel):
    def __init__(self):

        self.quoteId: str
        self.comment: str
