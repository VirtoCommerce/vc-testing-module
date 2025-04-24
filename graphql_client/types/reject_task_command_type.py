from pydantic import BaseModel


class RejectTaskCommandType(BaseModel):
    def __init__(self):

        self.id: str
