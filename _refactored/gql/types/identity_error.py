from gql.types.base import GqlModel


class IdentityError(GqlModel):
    code: str | None = None
    parameter: str | None = None
    description: str | None = None
