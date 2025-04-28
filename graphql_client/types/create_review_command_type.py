from pydantic import BaseModel


class CreateReviewCommandType(BaseModel):
    def __init__(self):

        self.storeId: str
        self.entityId: str
        self.entityType: str
        self.review: str
        self.rating: int
        self.imageUrls: list[str] | None
