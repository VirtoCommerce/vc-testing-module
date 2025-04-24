from pydantic import BaseModel


class ConfigurableProductOptionInput(BaseModel):
    def __init__(self):

        self.productId: str
        self.quantity: int
