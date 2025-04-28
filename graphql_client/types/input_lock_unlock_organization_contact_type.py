from pydantic import BaseModel


class InputLockUnlockOrganizationContactType(BaseModel):
    def __init__(self):

        self.userId: str | None
