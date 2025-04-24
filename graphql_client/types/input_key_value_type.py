from pydantic import BaseModel


class InputKeyValueType(BaseModel):
    def __init__(self):

        self.key: str
        self.value: str | None
