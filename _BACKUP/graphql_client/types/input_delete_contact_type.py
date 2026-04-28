from pydantic import BaseModel


class InputDeleteContactType(BaseModel):
    def __init__(self):

        self.contactId: str
