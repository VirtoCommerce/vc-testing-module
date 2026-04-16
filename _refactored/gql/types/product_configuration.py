from .base import GqlModel
from .configuration_section import ConfigurationSection


class ProductConfiguration(GqlModel):
    configuration_sections: list[ConfigurationSection] = []
