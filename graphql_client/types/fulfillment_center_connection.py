from pydantic import BaseModel


class FulfillmentCenterConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.fulfillment_center_type import FulfillmentCenterType
        from graphql_client.types.fulfillment_center_edge import FulfillmentCenterEdge
        from graphql_client.types.page_info import PageInfo

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[FulfillmentCenterEdge] | None
        self.items: list[FulfillmentCenterType] | None
