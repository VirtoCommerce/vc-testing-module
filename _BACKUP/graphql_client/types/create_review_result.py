from pydantic import BaseModel


class CreateReviewResult(BaseModel):
    def __init__(self):
        from graphql_client.types.review_validation_error_type import ReviewValidationErrorType

        self.id: str | None
        self.userName: str | None
        self.validationErrors: list[ReviewValidationErrorType]
