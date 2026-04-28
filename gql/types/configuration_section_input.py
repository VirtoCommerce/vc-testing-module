from .base import GqlModel
from .configurable_product_option_input import ConfigurableProductOptionInput


class ConfigurationSectionInput(GqlModel):
    section_id: str
    type: str
    option: ConfigurableProductOptionInput | None = None
    custom_text: str | None = None
    file_urls: list[str] | None = None
