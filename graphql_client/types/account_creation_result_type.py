from pydantic import BaseModel


class AccountCreationResultType(BaseModel):
    def __init__(self):
        from graphql_client.types.registration_error_type import RegistrationErrorType

        self.succeeded: bool
        self.requireEmailVerification: bool
        self.errors: list[RegistrationErrorType] | None
