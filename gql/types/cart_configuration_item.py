from .base import GqlModel


class CartConfigurationItem(GqlModel):
    id: str | None = None
    section_id: str | None = None
    type: str | None = None
    product_id: str | None = None
    name: str | None = None
    sku: str | None = None
    image_url: str | None = None
    quantity: int | None = None
    custom_text: str | None = None
    selected_for_checkout: bool | None = None
