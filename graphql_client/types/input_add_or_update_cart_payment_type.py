from pydantic import BaseModel


class InputAddOrUpdateCartPaymentType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_payment_type import InputPaymentType

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.payment: InputPaymentType
