from pydantic import BaseModel


class Asset(BaseModel):
    def __init__(self):

        self.id: str
        self.name: str | None
        self.mimeType: str | None
        self.size: int
        self.url: str
        self.relativeUrl: str | None
        self.typeId: str
        self.group: str | None
        self.description: str | None
        self.cultureName: str | None
