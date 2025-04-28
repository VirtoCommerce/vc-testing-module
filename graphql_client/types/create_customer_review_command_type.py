from pydantic import BaseModel


class CreateCustomerReviewCommandType(BaseModel):
    def __init__(self):

        self.storeId: str
        self.userId: str
        self.userName: str
        self.entityId: str
        self.entityType: str
        self.entityName: str
        self.title: str
        self.review: str
        self.rating: int
