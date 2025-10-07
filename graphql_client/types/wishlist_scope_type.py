from pydantic import BaseModel


class WishlistScopeType(BaseModel):
    Private = "Private"
    AnyoneAnonymous = "AnyoneAnonymous"
    AnyoneAuthorized = "AnyoneAuthorized"
    Organization = "Organization"
    User = "User"
