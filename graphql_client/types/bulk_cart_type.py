from pydantic import BaseModel


class BulkCartType(BaseModel):
    def __init__(self):
        from graphql_client.types.cart_type import CartType
        from graphql_client.types.validation_error_type import ValidationErrorType

        self.cart: CartType | None
        self.errors: list[ValidationErrorType] | None
