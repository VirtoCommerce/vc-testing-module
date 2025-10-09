from pydantic import BaseModel


class ResultType(BaseModel):
    def __init__(self):
        from graphql_client.types.result_validation_error_type import ResultValidationErrorType
        from graphql_client.types.result_status import ResultStatus

        self.isSuccess: bool
        self.successMessage: str | None
        self.status: ResultStatus
        self.errors: list[str]
        self.validationErrors: list[ResultValidationErrorType]
