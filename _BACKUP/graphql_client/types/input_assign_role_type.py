from pydantic import BaseModel


class InputAssignRoleType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_assign_permission_type import InputAssignPermissionType

        self.concurrencyStamp: str | None
        self.id: str
        self.name: str
        self.permissions: list[InputAssignPermissionType]
