from pydantic import BaseModel


class WishlistAccessType(BaseModel):
    Read = "Read"
    Write = "Write"
