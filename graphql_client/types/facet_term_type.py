from pydantic import BaseModel


class FacetTermType(BaseModel):
    def __init__(self):

        self.term: str
        self.count: int
        self.isSelected: bool
        self.label: str
