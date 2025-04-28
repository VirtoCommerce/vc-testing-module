from pydantic import BaseModel


class IdentityResultType(BaseModel):
    def __init__(self):
        from graphql_client.types.identity_error_type import IdentityErrorType

        self.succeeded: bool
        self.errors: list[IdentityErrorType] | None
