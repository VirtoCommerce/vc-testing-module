from pydantic import BaseModel


class ProductSuggestionsQueryResponseType(BaseModel):
    def __init__(self):

        self.suggestions: list[str] | None
