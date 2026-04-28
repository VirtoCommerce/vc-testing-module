from pydantic import BaseModel


class ApproveQuoteCommandType(BaseModel):
    def __init__(self):

        self.quoteId: str
