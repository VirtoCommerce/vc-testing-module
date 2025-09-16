from pydantic import BaseModel


class RangeFacetStatistics(BaseModel):
    def __init__(self):

        self.max: float | None
        self.min: float | None
