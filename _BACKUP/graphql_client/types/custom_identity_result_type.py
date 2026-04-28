from pydantic import BaseModel


class CustomIdentityResultType(BaseModel):
    def __init__(self):
        from graphql_client.types.identity_error_info_type import IdentityErrorInfoType

        self.succeeded: bool
        self.errors: list[IdentityErrorInfoType] | None
