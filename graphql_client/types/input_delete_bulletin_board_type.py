from pydantic import BaseModel


class InputDeleteBulletinBoardType(BaseModel):
    def __init__(self):

        self.storeId: str
        self.userId: str
