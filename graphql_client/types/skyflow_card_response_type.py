from pydantic import BaseModel


class SkyflowCardResponseType(BaseModel):
    def __init__(self):
        from graphql_client.types.skyflow_card_type import SkyflowCardType

        self.cards: list[SkyflowCardType] | None
