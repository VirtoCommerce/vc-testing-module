from pydantic import BaseModel


class ReviewValidationErrorType(BaseModel):
    def __init__(self):

        self.errorCode: str | None
        self.errorMessage: str | None
