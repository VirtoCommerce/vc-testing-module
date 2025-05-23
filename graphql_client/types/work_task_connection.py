from pydantic import BaseModel


class WorkTaskConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.work_task_edge import WorkTaskEdge
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.work_task_type import WorkTaskType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[WorkTaskEdge] | None
        self.items: list[WorkTaskType] | None
