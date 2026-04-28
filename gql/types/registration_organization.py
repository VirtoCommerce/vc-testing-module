from .base import GqlModel


class RegistrationOrganization(GqlModel):
    id: str
    name: str
    status: str | None = None
    owner_id: str | None = None
