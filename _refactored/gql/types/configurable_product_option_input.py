from .base import GqlModel


class ConfigurableProductOptionInput(GqlModel):
    product_id: str
    quantity: int
    selected_for_checkout: bool | None = None
