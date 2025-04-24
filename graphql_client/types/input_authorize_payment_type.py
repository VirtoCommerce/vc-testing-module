from pydantic import BaseModel


class InputAuthorizePaymentType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_key_value_type import InputKeyValueType

        self.orderId: str | None
        self.paymentId: str
        self.parameters: list[InputKeyValueType] | None
