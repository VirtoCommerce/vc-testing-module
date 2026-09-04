from datetime import datetime

from restapi.types.base import RestModel


class OrganizationMembership(RestModel):
    id: str | None = None
    user_id: str
    organization_id: str
    organization_name: str | None = None
    is_locked: bool = False
    lockout_end: datetime | None = None
    status: str | None = None
