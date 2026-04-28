from gql import gql
from graphql_client.types.work_task_connection import WorkTaskConnection


class TasksQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> WorkTaskConnection:
        query_string = f"""
            query tasks($after: String, $first: Int, $keyword: String, $sort: String, $responsibleId: String, $storeId: String, $startDueDate: DateTime, $endDueDate: DateTime, $isActive: Boolean, $completed: Boolean) {{
                tasks(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    responsibleId: $responsibleId,
                    storeId: $storeId,
                    startDueDate: $startDueDate,
                    endDueDate: $endDueDate,
                    isActive: $isActive,
                    completed: $completed
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["tasks"]
