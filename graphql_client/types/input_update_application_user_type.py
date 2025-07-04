from pydantic import BaseModel


class InputUpdateApplicationUserType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_assign_role_type import InputAssignRoleType
        from datetime import datetime

        self.accessFailedCount: int | None
        self.email: str
        self.id: str
        self.lockoutEnabled: bool | None
        self.lockoutEnd: datetime | None
        self.memberId: str | None
        self.phoneNumber: str | None
        self.phoneNumberConfirmed: bool | None
        self.photoUrl: str | None
        self.roles: list[InputAssignRoleType] | None
        self.storeId: str | None
        self.twoFactorEnabled: bool | None
        self.userName: str
        self.userType: str
        self.passwordHash: str | None
        self.securityStamp: str
