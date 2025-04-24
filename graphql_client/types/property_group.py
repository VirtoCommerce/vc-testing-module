from pydantic import BaseModel


class PropertyGroup(BaseModel):
    def __init__(self):

        self.id: str
        self.displayOrder: int | None
        self.name: str | None
        self.description: str | None
