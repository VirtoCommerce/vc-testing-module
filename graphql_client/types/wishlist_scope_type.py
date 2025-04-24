from pydantic import BaseModel


class WishlistScopeType(BaseModel):
    Private = "Private"
    Organization = "Organization"
