from .me_body import ME
from utils.normalize_graphql_payload import normalize_graphql_payload


class MeQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, user_id: str = None):
        variables = normalize_graphql_payload({"userId": user_id})

        return self.graphql_client.execute(ME, variable_values=variables)
