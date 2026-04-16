from pydantic import ConfigDict, Field

from gql.types.base import GqlModel


class CartItemInput(GqlModel):
    model_config = ConfigDict(alias_generator=None, populate_by_name=True)

    product_id: str = Field(serialization_alias="productId")
    quantity: int = 1
