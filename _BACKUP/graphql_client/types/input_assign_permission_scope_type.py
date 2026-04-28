from pydantic import BaseModel


class InputAssignPermissionScopeType(BaseModel):
    def __init__(self):

        self.scope: str
        self.type: str
