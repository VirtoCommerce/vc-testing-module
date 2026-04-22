from pydantic import BaseModel


class InputCreateApplicationUserType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_assign_role_type import InputAssignRoleType
        from graphql_client.types.input_application_user_login_type import InputApplicationUserLoginType
        from datetime import datetime

        self.createdBy: str | None
        self.createdDate: datetime | None
        self.email: str
        self.id: str | None
        self.lockoutEnabled: bool | None
        self.lockoutEnd: datetime | None
        self.logins: list[InputApplicationUserLoginType] | None
        self.memberId: str | None
        self.password: str | None
        self.phoneNumber: str | None
        self.phoneNumberConfirmed: bool | None
        self.photoUrl: str | None
        self.roles: list[InputAssignRoleType] | None
        self.storeId: str | None
        self.twoFactorEnabled: bool | None
        self.userName: str
        self.userType: str
        self.passwordExpired: bool | None
