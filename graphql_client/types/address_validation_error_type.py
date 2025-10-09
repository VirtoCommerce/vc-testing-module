from pydantic import BaseModel


class AddressValidationErrorType(BaseModel):
    def __init__(self):

        self.code: str | None
        self.message: str
