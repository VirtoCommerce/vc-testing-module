from pydantic import BaseModel


class OpusSearchDiagnosticsType(BaseModel):
    def __init__(self):
        from graphql_client.types.json import JSON
        from graphql_client.types.elastic_search_explain_hit_type import ElasticSearchExplainHitType

        self.requestId: str | None
        self.appSearchQuery: JSON | None
        self.elasticSearchQueryString: str | None
        self.elasticSearchQueryBody: JSON | None
        self.took: int | None
        self.maxScore: float | None
        self.hits: list[ElasticSearchExplainHitType] | None
