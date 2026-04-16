from gql.types.identity_error import IdentityError
from gql.types.base import GqlModel


class IdentityResult(GqlModel):
    succeeded: bool
    errors: list[IdentityError] = []
