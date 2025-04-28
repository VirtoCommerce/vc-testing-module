from pydantic import BaseModel


class FilterFacet(BaseModel):
    def __init__(self):
        from graphql_client.types.facet_types import FacetTypes

        self.name: str
        self.label: str
        self.facetType: FacetTypes
        self.count: int
