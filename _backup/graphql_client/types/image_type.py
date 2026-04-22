from pydantic import BaseModel


class ImageType(BaseModel):
    def __init__(self):

        self.id: str
        self.name: str | None
        self.group: str | None
        self.url: str
        self.relativeUrl: str | None
        self.sortOrder: int
        self.cultureName: str | None
        self.description: str | None
