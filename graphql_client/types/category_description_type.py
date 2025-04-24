from pydantic import BaseModel


class CategoryDescriptionType(BaseModel):
    def __init__(self):

        self.id: str
        self.descriptionType: str | None
        self.content: str | None
        self.languageCode: str | None
