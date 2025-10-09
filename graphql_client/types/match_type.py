from pydantic import BaseModel


class MatchType(BaseModel):
    def __init__(self):

        self.startOffset: int
        self.endOffset: int
