from pydantic import BaseModel


class BulletinBoardType(BaseModel):
    def __init__(self):
        from graphql_client.types.bulletin_board_file_type import BulletinBoardFileType
        from datetime import datetime

        self.id: str
        self.modifiedDate: datetime | None
        self.number: str
        self.title: str
        self.text: str | None
        self.isDefault: bool
        self.isReadOnly: bool
        self.isNew: bool
        self.images: list[BulletinBoardFileType]
        self.files: list[BulletinBoardFileType]
