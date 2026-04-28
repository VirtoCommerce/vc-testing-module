from restapi.types.base import RestModel


class Member(RestModel):
    id: str
    name: str
    member_type: str | None = None
