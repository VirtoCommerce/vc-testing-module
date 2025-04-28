from pydantic import BaseModel


class LocalizedSettingResponseType(BaseModel):
    def __init__(self):
        from graphql_client.types.key_value_type import KeyValueType

        self.items: list[KeyValueType] | None
