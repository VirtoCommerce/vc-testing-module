from .base import GqlModel


class RegistrationAccount(GqlModel):
    id: str
    username: str
    email: str
    status: str | None = None
