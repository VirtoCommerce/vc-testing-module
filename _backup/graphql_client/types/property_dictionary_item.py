from pydantic import BaseModel


class PropertyDictionaryItem(BaseModel):
    def __init__(self):

        self.id: str
        self.value: str | None
        self.colorCode: str
        self.sortOrder: int
