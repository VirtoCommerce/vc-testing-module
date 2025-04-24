from pydantic import BaseModel


class ChangeQuoteCommentCommandType(BaseModel):
    def __init__(self):

        self.quoteId: str
        self.comment: str
