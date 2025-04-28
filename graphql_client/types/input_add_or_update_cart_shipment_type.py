from pydantic import BaseModel


class InputAddOrUpdateCartShipmentType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_shipment_type import InputShipmentType

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.shipment: InputShipmentType
