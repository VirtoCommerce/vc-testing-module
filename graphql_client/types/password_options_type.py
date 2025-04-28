from pydantic import BaseModel


class PasswordOptionsType(BaseModel):
    def __init__(self):

        self.requiredLength: int
        self.requiredUniqueChars: int
        self.requireNonAlphanumeric: bool
        self.requireLowercase: bool
        self.requireUppercase: bool
        self.requireDigit: bool
