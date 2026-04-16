from .base import GqlModel


class RegistrationContact(GqlModel):
    id: str
    first_name: str
    last_name: str
    status: str | None = None
