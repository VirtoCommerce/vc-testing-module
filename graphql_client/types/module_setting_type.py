from pydantic import BaseModel


class ModuleSettingType(BaseModel):
    def __init__(self):

        self.name: str
        self.value: str | None
