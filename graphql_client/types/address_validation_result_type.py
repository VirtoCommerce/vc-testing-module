from pydantic import BaseModel


class AddressValidationResultType(BaseModel):
    def __init__(self):
        from graphql_client.types.address_validation_error_type import AddressValidationErrorType
        from graphql_client.types.opus_cart_address_type import OpusCartAddressType
        from graphql_client.types.opus_cart_address_type import OpusCartAddressType

        self.address: OpusCartAddressType
        self.validatedAddresses: list[OpusCartAddressType] | None
        self.addressIsValid: bool
        self.messages: list[AddressValidationErrorType] | None
