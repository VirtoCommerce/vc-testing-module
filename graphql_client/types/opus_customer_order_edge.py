from pydantic import BaseModel


class OpusCustomerOrderEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_customer_order_type import OpusCustomerOrderType

        self.cursor: str
        self.node: OpusCustomerOrderType | None
