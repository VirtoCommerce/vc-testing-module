from .base import GqlModel
from .cart import Cart


class CartWithList(GqlModel):
    cart: Cart
    list: Cart
