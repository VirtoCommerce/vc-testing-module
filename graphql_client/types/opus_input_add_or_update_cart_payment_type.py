from pydantic import BaseModel


class OpusInputAddOrUpdateCartPaymentType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_payment_type import InputPaymentType
        from graphql_client.types.opus_input_payment_type import OpusInputPaymentType

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.payment: InputPaymentType
        self.paymentExtension: OpusInputPaymentType | None
