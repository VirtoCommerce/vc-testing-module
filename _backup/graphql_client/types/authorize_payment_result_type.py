from pydantic import BaseModel


class AuthorizePaymentResultType(BaseModel):
    def __init__(self):

        self.isSuccess: bool
        self.errorMessage: str | None
