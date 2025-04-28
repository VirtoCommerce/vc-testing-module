from pydantic import BaseModel


class OrderConfigurationItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.order_configuration_item_file_type import OrderConfigurationItemFileType

        self.id: str
        self.name: str | None
        self.type: str
        self.customText: str | None
        self.files: list[OrderConfigurationItemFileType] | None
