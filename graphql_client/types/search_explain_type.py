from pydantic import BaseModel


class SearchExplainType(BaseModel):
    def __init__(self):

        self.field: str | None
        self.feature: str | None
        self.score: float | None
        self.freq: float | None
        self.boost: float | None
        self.idf: float | None
        self.tf: float | None
