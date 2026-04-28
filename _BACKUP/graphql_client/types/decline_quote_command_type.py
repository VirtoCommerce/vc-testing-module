from pydantic import BaseModel


class DeclineQuoteCommandType(BaseModel):
    def __init__(self):

        self.quoteId: str
