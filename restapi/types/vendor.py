from restapi.types.base import RestModel


class Vendor(RestModel):
    id: str
    name: str | None = None
    member_type: str | None = None
