from pydantic import BaseModel


class ProductPickupLocationEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.product_pickup_location import ProductPickupLocation

        self.cursor: str
        self.node: ProductPickupLocation | None
