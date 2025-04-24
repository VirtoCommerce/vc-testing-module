from pydantic import BaseModel


class ConfigurationItemsResponseType(BaseModel):
    def __init__(self):
        from graphql_client.types.cart_configuration_item_type import CartConfigurationItemType

        self.configurationItems: list[CartConfigurationItemType] | None
