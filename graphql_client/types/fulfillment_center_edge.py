from pydantic import BaseModel


class FulfillmentCenterEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.fulfillment_center_type import FulfillmentCenterType

        self.cursor: str
        self.node: FulfillmentCenterType | None
