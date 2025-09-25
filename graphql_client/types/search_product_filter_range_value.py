from pydantic import BaseModel


class SearchProductFilterRangeValue(BaseModel):
    def __init__(self):

        self.lower: str | None
        self.upper: str | None
        self.includeLowerBound: bool
        self.includeUpperBound: bool
