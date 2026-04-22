from pydantic import BaseModel


class InputAddOrUpdateCartAddressType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_address_type import InputAddressType

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.address: InputAddressType
