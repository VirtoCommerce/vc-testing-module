from pydantic import BaseModel


class InputResendUserInvitationType(BaseModel):
    def __init__(self):

        self.userId: str
        self.storeId: str
        self.urlSuffix: str
        self.message: str | None
