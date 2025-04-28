from pydantic import BaseModel


class VideoEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.video_type import VideoType

        self.cursor: str
        self.node: VideoType | None
