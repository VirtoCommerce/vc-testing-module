from restapi.types.base import RestModel


class Organization(RestModel):
    id: str
    name: str
    member_type: str | None = None
