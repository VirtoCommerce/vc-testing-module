from pydantic import BaseModel


class ModuleSettingsType(BaseModel):
    def __init__(self):
        from graphql_client.types.module_setting_type import ModuleSettingType

        self.moduleId: str
        self.settings: list[ModuleSettingType]
