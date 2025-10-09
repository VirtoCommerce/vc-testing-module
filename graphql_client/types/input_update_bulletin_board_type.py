from pydantic import BaseModel


class InputUpdateBulletinBoardType(BaseModel):
    def __init__(self):
        from graphql_client.types.bulletin_board_file_upload_request_type import BulletinBoardFileUploadRequestType

        self.storeId: str
        self.userId: str
        self.title: str | None
        self.text: str
        self.files: list[BulletinBoardFileUploadRequestType]
        self.images: list[BulletinBoardFileUploadRequestType]
