from pydantic import BaseModel


class KeyValueType(BaseModel):
    def __init__(self):

        self.key: str
        self.value: str | None
