from pydantic import BaseModel


class ContractType(BaseModel):
    def __init__(self):
        from datetime import datetime
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType

        self.id: str
        self.name: str
        self.code: str
        self.description: str | None
        self.vendorId: str | None
        self.storeId: str | None
        self.status: str | None
        self.startDate: datetime | None
        self.endDate: datetime | None
        self.dynamicProperties: list[DynamicPropertyValueType] | None
