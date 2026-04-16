from .base import GqlModel
from .user import User


class Contact(GqlModel):
    id: str
    first_name: str
    last_name: str
    full_name: str
    status: str | None = None
    organization_id: str | None = None
    organizations_ids: list[str] = []
    security_accounts: list[User] = []
