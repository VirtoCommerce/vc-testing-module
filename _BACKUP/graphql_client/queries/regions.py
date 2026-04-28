from gql import gql
from graphql_client.types.country_region_type import CountryRegionType


class RegionsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> list[CountryRegionType]:
        query_string = f"""
            query regions($countryId: String!) {{
                regions(
                    countryId: $countryId
                )
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["regions"]
