from pydantic import BaseModel


class FulfillmentCenterType(BaseModel):
    def __init__(self):
        from graphql_client.types.fulfillment_center_type import FulfillmentCenterType
        from graphql_client.types.fulfillment_center_address_type import FulfillmentCenterAddressType

        self.id: str
        self.name: str | None
        self.description: str | None
        self.outerId: str | None
        self.geoLocation: str | None
        self.shortDescription: str | None
        self.address: FulfillmentCenterAddressType | None
        self.nearest: list[FulfillmentCenterType] | None
