from pydantic import BaseModel


class CustomerOrderEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.customer_order_type import CustomerOrderType

        self.cursor: str
        self.node: CustomerOrderType | None
