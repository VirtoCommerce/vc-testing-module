from pydantic import BaseModel


class InputRemoveMemberFromOrganizationType(BaseModel):
    def __init__(self):

        self.contactId: str | None
        self.organizationId: str | None
