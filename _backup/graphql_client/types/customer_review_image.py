from pydantic import BaseModel


class CustomerReviewImage(BaseModel):
    def __init__(self):

        self.id: str
        self.url: str
        self.name: str
