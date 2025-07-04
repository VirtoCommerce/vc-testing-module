from pydantic import BaseModel


class PickupLocationConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.pickup_location_edge import PickupLocationEdge
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.pickup_location_type import PickupLocationType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[PickupLocationEdge] | None
        self.items: list[PickupLocationType] | None
