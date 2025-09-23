from pydantic import BaseModel


class VariationType(BaseModel):
    def __init__(self):
        from graphql_client.types.price_type import PriceType
        from graphql_client.types.price_type import PriceType
        from graphql_client.types.image_type import ImageType
        from graphql_client.types.asset import Asset
        from graphql_client.types.property import Property
        from graphql_client.types.outline_type import OutlineType
        from graphql_client.types.common_vendor import CommonVendor
        from graphql_client.types.availability_data import AvailabilityData
        from graphql_client.types.rating import Rating

        self.id: str
        self.name: str
        self.code: str
        self.productType: str | None
        self.minQuantity: int | None
        self.maxQuantity: int | None
        self.packSize: int | None
        self.availabilityData: AvailabilityData
        self.images: list[ImageType]
        self.price: PriceType
        self.prices: list[PriceType]
        self.properties: list[Property]
        self.assets: list[Asset]
        self.outlines: list[OutlineType] | None
        self.slug: str | None
        self.vendor: CommonVendor | None
        self.rating: Rating | None
