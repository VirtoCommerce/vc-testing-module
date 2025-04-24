from pydantic import BaseModel


class InputDynamicPropertyValueType(BaseModel):
    def __init__(self):

        self.name: str
        self.value: str | None
        self.cultureName: str | None
