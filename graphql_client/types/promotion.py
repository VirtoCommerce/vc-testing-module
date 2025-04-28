from pydantic import BaseModel


class Promotion(BaseModel):
    def __init__(self):

        self.id: str
        self.name: str
        self.description: str | None
        self.type: str | None
