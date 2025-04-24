from pydantic import BaseModel


class PageInfo(BaseModel):
    def __init__(self):

        self.hasNextPage: bool
        self.hasPreviousPage: bool
        self.startCursor: str | None
        self.endCursor: str | None
