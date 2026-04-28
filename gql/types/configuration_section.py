from .base import GqlModel
from .configuration_line_item import ConfigurationLineItem


class ConfigurationSection(GqlModel):
    id: str
    name: str | None = None
    description: str | None = None
    is_required: bool
    type: str
    allow_custom_text: bool
    allow_text_options: bool
    max_length: int | None = None
    options: list[ConfigurationLineItem] = []
