from pydantic import BaseModel


class RangeFacet(BaseModel):
    def __init__(self):
        from graphql_client.types.facet_types import FacetTypes
        from graphql_client.types.facet_range_type import FacetRangeType

        self.name: str
        self.label: str
        self.facetType: FacetTypes
        self.ranges: list[FacetRangeType]
