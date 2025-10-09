from pydantic import BaseModel


class AddressSuggestionResponseType(BaseModel):
    def __init__(self):
        from graphql_client.types.suggestion_type import SuggestionType

        self.suggestions: list[SuggestionType]
