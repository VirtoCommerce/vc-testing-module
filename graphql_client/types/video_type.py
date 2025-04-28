from pydantic import BaseModel


class VideoType(BaseModel):
    def __init__(self):
        from datetime import datetime

        self.name: str
        self.description: str
        self.uploadDate: datetime | None
        self.thumbnailUrl: str
        self.contentUrl: str
        self.embedUrl: str | None
        self.duration: str | None
        self.cultureName: str | None
        self.ownerId: str
        self.ownerType: str
        self.sortOrder: int
