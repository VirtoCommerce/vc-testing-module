from .base import GqlModel


class MenuLink(GqlModel):
    title: str
    url: str | None = None
    priority: int | None = None
