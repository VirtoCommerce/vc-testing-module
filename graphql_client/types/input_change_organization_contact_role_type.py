from pydantic import BaseModel


class InputChangeOrganizationContactRoleType(BaseModel):
    def __init__(self):

        self.userId: str | None
        self.roleIds: list[str] | None
