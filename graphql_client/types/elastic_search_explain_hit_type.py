from pydantic import BaseModel


class ElasticSearchExplainHitType(BaseModel):
    def __init__(self):
        from graphql_client.types.json import JSON

        self.id: str
        self.index: str
        self.score: float | None
        self.explanation: JSON | None
