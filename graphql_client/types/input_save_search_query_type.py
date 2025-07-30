from pydantic import BaseModel


class InputSaveSearchQueryType(BaseModel):
    def __init__(self):

        self.storeId: str
        self.query: str
