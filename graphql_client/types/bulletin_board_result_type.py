from pydantic import BaseModel


class BulletinBoardResultType(BaseModel):
    def __init__(self):
        from graphql_client.types.bulletin_board_type import BulletinBoardType
        from graphql_client.types.result_validation_error_type import ResultValidationErrorType
        from graphql_client.types.result_status import ResultStatus

        self.value: BulletinBoardType | None
        self.isSuccess: bool
        self.successMessage: str | None
        self.status: ResultStatus
        self.errors: list[str]
        self.validationErrors: list[ResultValidationErrorType]
