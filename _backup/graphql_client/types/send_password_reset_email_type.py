from pydantic import BaseModel


class SendPasswordResetEmailResultType(BaseModel):
    sendPasswordResetEmail: bool
