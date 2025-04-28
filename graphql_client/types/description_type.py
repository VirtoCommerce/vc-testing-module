from pydantic import BaseModel


class DescriptionType(BaseModel):
    def __init__(self):

        self.id: str
        self.reviewType: str | None
        self.content: str | None
        self.languageCode: str | None
