from pydantic import BaseModel


class InputAddItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType
        from datetime import datetime
        from decimal import Decimal
        from graphql_client.types.configuration_section_input import ConfigurationSectionInput

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.productId: str
        self.quantity: int
        self.price: Decimal | None
        self.comment: str | None
        self.dynamicProperties: list[InputDynamicPropertyValueType] | None
        self.configurationSections: list[ConfigurationSectionInput] | None
        self.createdDate: datetime | None
