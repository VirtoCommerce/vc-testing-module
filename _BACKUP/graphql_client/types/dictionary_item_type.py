from pydantic import BaseModel


class DictionaryItemType(BaseModel):
    def __init__(self):

        self.id: str
        self.name: str
        self.label: str | None
