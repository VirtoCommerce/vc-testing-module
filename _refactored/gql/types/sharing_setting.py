from .base import GqlModel


class SharingSetting(GqlModel):
    id: str
    scope: str | None = None
