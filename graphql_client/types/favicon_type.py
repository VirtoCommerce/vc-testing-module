from pydantic import BaseModel


class FaviconType(BaseModel):
    def __init__(self):

        self.rel: str | None
        self.type: str | None
        self.sizes: str | None
        self.href: str | None
