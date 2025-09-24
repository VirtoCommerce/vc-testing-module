from pydantic import BaseModel


class SearchProductFilterResult(BaseModel):
    def __init__(self):
        from graphql_client.types.search_product_filter_range_value import SearchProductFilterRangeValue
        from graphql_client.types.search_product_filter_value import SearchProductFilterValue

        self.name: str
        self.filterType: str
        self.isGenerated: bool
        self.label: str | None
        self.termValues: list[SearchProductFilterValue] | None
        self.rangeValues: list[SearchProductFilterRangeValue] | None
