from pydantic import BaseModel


class InputInviteUserType(BaseModel):
    def __init__(self):

        self.storeId: str
        self.organizationId: str | None
        self.urlSuffix: str | None
        self.emails: list[str]
        self.message: str | None
        self.roleIds: list[str] | None
        self.customerOrderId: str | None
