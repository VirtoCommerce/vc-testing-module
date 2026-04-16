from gql.types.base import GqlModel


class Role(GqlModel):
    id: str
    name: str
    normalized_name: str
