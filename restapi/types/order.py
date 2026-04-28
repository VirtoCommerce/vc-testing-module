from restapi.types.base import RestModel


class OrderLineItem(RestModel):
    id: str | None = None
    product_id: str | None = None
    sku: str | None = None
    name: str | None = None
    quantity: int | None = None


class CustomerOrder(RestModel):
    id: str
    number: str
    store_id: str
    customer_id: str
    status: str | None = None
    items: list[OrderLineItem] = []
