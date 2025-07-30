from pydantic import BaseModel


class SearchHistoryResultType(BaseModel):
    def __init__(self):

        self.queries: list[str] | None
