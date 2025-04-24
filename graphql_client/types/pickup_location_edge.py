from pydantic import BaseModel


class PickupLocationEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.pickup_location_type import PickupLocationType

        self.cursor: str
        self.node: PickupLocationType | None
