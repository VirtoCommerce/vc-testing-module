from pydantic import BaseModel


class ConfirmTaskCommandType(BaseModel):
    def __init__(self):

        self.id: str
