from pydantic import BaseModel


class PaymentInEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.payment_in_type import PaymentInType

        self.cursor: str
        self.node: PaymentInType | None
