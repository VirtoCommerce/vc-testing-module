from pydantic import BaseModel


class BulletinBoardFileUploadRequestType(BaseModel):
    def __init__(self):

        self.id: str
        self.url: str
        self.name: str
        self.contentType: str
        self.size: int
