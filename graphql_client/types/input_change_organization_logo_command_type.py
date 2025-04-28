from pydantic import BaseModel


class InputChangeOrganizationLogoCommandType(BaseModel):
    def __init__(self):

        self.organizationId: str
        self.logoUrl: str | None
