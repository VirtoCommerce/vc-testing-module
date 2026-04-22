from pydantic import BaseModel


class CategoryEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.category import Category

        self.cursor: str
        self.node: Category | None
