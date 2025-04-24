from pydantic import BaseModel


class CartConfigurationItemFileType(BaseModel):
    def __init__(self):

        self.url: str
        self.name: str
        self.size: int
        self.contentType: str | None
