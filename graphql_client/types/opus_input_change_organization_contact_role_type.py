from pydantic import BaseModel


class OpusInputChangeOrganizationContactRoleType(BaseModel):
    def __init__(self):

        self.userId: str
        self.roleId: str
        self.removeRole: bool | None
