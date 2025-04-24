from pydantic import BaseModel


class InputRegisterByInvitationType(BaseModel):
    def __init__(self):

        self.userId: str
        self.token: str
        self.firstName: str
        self.lastName: str
        self.phone: str | None
        self.username: str
        self.password: str
        self.customerOrderId: str | None
