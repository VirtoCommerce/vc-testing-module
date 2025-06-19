from pydantic import BaseModel


class CustomerReview(BaseModel):
    def __init__(self):
        from graphql_client.types.customer_review_status import CustomerReviewStatus
        from datetime import datetime
        from graphql_client.types.customer_review_image import CustomerReviewImage

        self.id: str
        self.createdDate: datetime
        self.modifiedDate: datetime | None
        self.storeId: str
        self.userId: str
        self.userName: str
        self.entityId: str
        self.entityType: str
        self.entityName: str
        self.title: str | None
        self.review: str
        self.rating: int
        self.reviewStatus: CustomerReviewStatus | None
        self.images: list[CustomerReviewImage] | None
