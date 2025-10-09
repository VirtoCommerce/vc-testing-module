from pydantic import BaseModel


class BulletinBoardFileType(BaseModel):
    def __init__(self):

        self.id: str
        self.url: str
        self.name: str
        self.contentType: str | None
        self.size: int
