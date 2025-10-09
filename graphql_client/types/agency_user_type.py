from pydantic import BaseModel


class AgencyUserType(BaseModel):
    def __init__(self):
        from graphql_client.types.role_type import RoleType

        self.id: str
        self.fullName: str
        self.firstName: str
        self.lastName: str
        self.userName: str
        self.role: str
        self.isLockedOut: bool
        self.orderApproverName: str
        self.orderApproverId: str
        self.objectType: str
        self.roles: list[RoleType] | None
