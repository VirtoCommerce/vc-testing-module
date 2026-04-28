from pydantic import BaseModel


class QuoteConfigurationItemFileType(BaseModel):
    def __init__(self):

        self.url: str
        self.name: str
        self.size: int
        self.contentType: str | None
