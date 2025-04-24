from pydantic import BaseModel


class AddAddressToFavoritesCommandType(BaseModel):
    def __init__(self):

        self.addressId: str
