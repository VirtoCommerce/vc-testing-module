from pydantic import BaseModel


class RemoveAddressFromFavoritesCommandType(BaseModel):
    def __init__(self):

        self.addressId: str
