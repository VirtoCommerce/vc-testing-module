from pydantic import BaseModel


class ChangeOrganizationLogoResultType(BaseModel):
    def __init__(self):

        self.isSuccess: bool
        self.errorMessage: str | None
