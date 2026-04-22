from pydantic import BaseModel


class DeleteFileCommandType(BaseModel):
    def __init__(self):

        self.id: str
