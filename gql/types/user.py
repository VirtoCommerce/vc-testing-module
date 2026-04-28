from gql.types.base import GqlModel
from gql.types.role import Role


class User(GqlModel):
    id: str
    user_name: str
    email: str | None = None
    email_confirmed: bool
    is_administrator: bool
    member_id: str | None = None
    store_id: str | None = None
    roles: list[Role] = []
