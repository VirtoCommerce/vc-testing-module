from pydantic import BaseModel


class InputAddOrUpdateOrderPaymentType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_order_payment_type import InputOrderPaymentType

        self.orderId: str
        self.payment: InputOrderPaymentType
