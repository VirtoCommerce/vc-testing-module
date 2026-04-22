from pydantic import BaseModel


class FacetTypes(BaseModel):
    TERMS = "TERMS"
    RANGE = "RANGE"
    FILTER = "FILTER"
