from pydantic import BaseModel


class UserType(BaseModel):
    def __init__(self):
        from datetime import datetime
        from graphql_client.types.role_type import RoleType
        from graphql_client.types.user_type import UserType
        from graphql_client.types.contact_type import ContactType

        self.accessFailedCount: int
        self.createdBy: str | None
        self.createdDate: datetime | None
        self.email: str | None
        self.emailConfirmed: bool
        self.id: str
        self.isAdministrator: bool
        self.lockoutEnabled: bool
        self.lockoutEnd: datetime | None
        self.memberId: str | None
        self.modifiedBy: str | None
        self.modifiedDate: datetime | None
        self.normalizedEmail: str | None
        self.normalizedUserName: str | None
        self.phoneNumber: str | None
        self.phoneNumberConfirmed: bool
        self.photoUrl: str | None
        self.roles: list[RoleType] | None
        self.permissions: list[str] | None
        self.securityStamp: str
        self.storeId: str | None
        self.twoFactorEnabled: bool
        self.userName: str
        self.userType: str | None
        self.passwordExpired: bool
        self.forcePasswordChange: bool | None
        self.passwordExpiryInDays: int | None
        self.contact: ContactType | None
        self.lockedState: bool | None
        self.operator: UserType | None
