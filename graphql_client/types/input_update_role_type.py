from pydantic import BaseModel


class InputUpdateRoleType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_update_role_inner_type import InputUpdateRoleInnerType

        self.role: InputUpdateRoleInnerType
