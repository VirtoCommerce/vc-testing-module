from pydantic import BaseModel


class CommonVendor(BaseModel):
    def __init__(self):
        from graphql_client.types.rating import Rating

        self.id: str
        self.name: str
        self.rating: Rating | None
