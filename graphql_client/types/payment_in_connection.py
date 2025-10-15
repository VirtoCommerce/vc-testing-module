from pydantic import BaseModel


class PaymentInConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.payment_in_edge import PaymentInEdge
        from graphql_client.types.payment_in_type import PaymentInType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[PaymentInEdge] | None
        self.items: list[PaymentInType] | None
