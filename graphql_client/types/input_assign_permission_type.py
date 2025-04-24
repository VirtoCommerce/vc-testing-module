from pydantic import BaseModel


class InputAssignPermissionType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_assign_permission_scope_type import InputAssignPermissionScopeType

        self.assignedScopes: list[InputAssignPermissionScopeType] | None
        self.name: str
