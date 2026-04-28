from restapi.types.base import RestModel


class User(RestModel):
    id: str
    user_name: str
    email: str | None = None
    user_type: str | None = None
