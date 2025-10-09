from pydantic import BaseModel


class ResultValidationErrorType(BaseModel):
    def __init__(self):
        from graphql_client.types.validation_severity import ValidationSeverity

        self.errorCode: str
        self.errorMessage: str | None
        self.identifier: str | None
        self.severity: ValidationSeverity
