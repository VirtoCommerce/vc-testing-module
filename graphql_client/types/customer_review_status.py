from pydantic import BaseModel


class CustomerReviewStatus(BaseModel):
    NEW = "NEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
