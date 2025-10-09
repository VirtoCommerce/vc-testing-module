from pydantic import BaseModel


class ValidationSeverity(BaseModel):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
