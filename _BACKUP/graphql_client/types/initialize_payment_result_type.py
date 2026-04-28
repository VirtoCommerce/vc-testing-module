from pydantic import BaseModel


class InitializePaymentResultType(BaseModel):
    def __init__(self):
        from graphql_client.types.key_value_type import KeyValueType

        self.isSuccess: bool
        self.errorMessage: str | None
        self.storeId: str | None
        self.paymentId: str | None
        self.orderId: str | None
        self.orderNumber: str | None
        self.paymentMethodCode: str | None
        self.paymentActionType: str | None
        self.actionRedirectUrl: str | None
        self.actionHtmlForm: str | None
        self.publicParameters: list[KeyValueType] | None
