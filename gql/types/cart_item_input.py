from pydantic import ConfigDict, Field

from gql.types.base import GqlModel
from gql.types.configuration_section_input import ConfigurationSectionInput


class CartItemInput(GqlModel):
    model_config = ConfigDict(alias_generator=None, populate_by_name=True)

    product_id: str = Field(serialization_alias="productId")
    quantity: int = 1
    configuration_sections: list[ConfigurationSectionInput] | None = Field(
        default=None, serialization_alias="configurationSections"
    )
