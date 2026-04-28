from pydantic import BaseModel


class SearchProductFilterValue(BaseModel):
    def __init__(self):

        self.value: str
        self.label: str | None
