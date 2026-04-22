from pydantic import BaseModel


class CustomerReviewConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.customer_review import CustomerReview
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.customer_review_edge import CustomerReviewEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[CustomerReviewEdge] | None
        self.items: list[CustomerReview] | None
