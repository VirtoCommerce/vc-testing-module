from pydantic import BaseModel


class ValidationErrorType(BaseModel):
    def __init__(self):
        from graphql_client.types.error_parameter_type import ErrorParameterType

        self.errorCode: str | None
        self.errorMessage: str | None
        self.objectId: str | None
        self.objectType: str | None
        self.errorParameters: list[ErrorParameterType] | None
