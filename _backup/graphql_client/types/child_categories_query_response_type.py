from pydantic import BaseModel


class ChildCategoriesQueryResponseType(BaseModel):
    def __init__(self):
        from graphql_client.types.category import Category

        self.childCategories: list[Category] | None
