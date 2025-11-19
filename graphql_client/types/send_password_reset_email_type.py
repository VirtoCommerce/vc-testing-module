from pydantic import BaseModel


class SendPasswordResetEmailType(BaseModel):
    def __init__(self):
        self.sendPasswordResetEmail: bool
      