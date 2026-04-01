from .base import GqlModel


class Language(GqlModel):
    culture_name: str
    native_name: str | None = None
