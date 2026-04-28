from restapi.types.base import RestModel


class Employee(RestModel):
    id: str
    first_name: str | None = None
    last_name: str | None = None
    name: str | None = None
    member_type: str | None = None
