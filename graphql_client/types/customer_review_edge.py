from pydantic import BaseModel


class CustomerReviewEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.customer_review import CustomerReview

        self.cursor: str
        self.node: CustomerReview | None
