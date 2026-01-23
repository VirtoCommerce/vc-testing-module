from pydantic import BaseModel


class BuilderPageItemType(BaseModel):
    def __init__(self):

        self.permalink: str | None
        self.content: str | None
