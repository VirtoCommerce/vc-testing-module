from pydantic import BaseModel


class SuggestionType(BaseModel):
    def __init__(self):
        from graphql_client.types.core_address_type import CoreAddressType
        from graphql_client.types.match_type import MatchType

        self.text: str
        self.address: CoreAddressType | None
        self.matches: list[MatchType] | None
