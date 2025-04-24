from pydantic import BaseModel


class RoleType(BaseModel):
    def __init__(self):

        self.description: str | None
        self.id: str
        self.name: str
        self.normalizedName: str
        self.permissions: list[str]
