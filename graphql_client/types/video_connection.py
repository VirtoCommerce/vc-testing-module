from pydantic import BaseModel


class VideoConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.video_edge import VideoEdge
        from graphql_client.types.video_type import VideoType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[VideoEdge] | None
        self.items: list[VideoType] | None
