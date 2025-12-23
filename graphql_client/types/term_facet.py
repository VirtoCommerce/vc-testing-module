from pydantic import BaseModel


class TermFacet(BaseModel):
    def __init__(self):
        from graphql_client.types.facet_types import FacetTypes
        from graphql_client.types.facet_term_type import FacetTermType

        self.name: str
        self.label: str
        self.order: int | None
        self.facetType: FacetTypes
        self.terms: list[FacetTermType]
