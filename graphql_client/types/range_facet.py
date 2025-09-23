from pydantic import BaseModel


class RangeFacet(BaseModel):
    def __init__(self):
        from graphql_client.types.range_facet_statistics import RangeFacetStatistics
        from graphql_client.types.facet_range_type import FacetRangeType
        from graphql_client.types.facet_types import FacetTypes

        self.name: str
        self.label: str
        self.order: int | None
        self.facetType: FacetTypes
        self.ranges: list[FacetRangeType]
        self.statistics: RangeFacetStatistics | None
