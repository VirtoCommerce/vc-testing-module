from pydantic import BaseModel


class Product(BaseModel):
    def __init__(self):
        from graphql_client.types.seo_info import SeoInfo
        from graphql_client.types.property import Property
        from graphql_client.types.variation_type import VariationType
        from graphql_client.types.price_type import PriceType
        from graphql_client.types.description_type import DescriptionType
        from graphql_client.types.price_type import PriceType
        from graphql_client.types.video_connection import VideoConnection
        from decimal import Decimal
        from graphql_client.types.common_vendor import CommonVendor
        from graphql_client.types.asset import Asset
        from graphql_client.types.availability_data import AvailabilityData
        from graphql_client.types.category import Category
        from graphql_client.types.variation_type import VariationType
        from graphql_client.types.rating import Rating
        from graphql_client.types.breadcrumb import Breadcrumb
        from graphql_client.types.image_type import ImageType
        from graphql_client.types.brand_type import BrandType
        from graphql_client.types.description_type import DescriptionType
        from graphql_client.types.product_association_connection import ProductAssociationConnection
        from graphql_client.types.outline_type import OutlineType

        self.id: str
        self.code: str
        self.catalogId: str | None
        self.productType: str | None
        self.minQuantity: int | None
        self.maxQuantity: int | None
        self.packSize: int
        self.relevanceScore: float | None
        self.isConfigurable: bool
        self.outline: str | None
        self.slug: str | None
        self.name: str
        self.seoInfo: SeoInfo
        self.descriptions: list[DescriptionType]
        self.description: DescriptionType | None
        self.category: Category | None
        self.imgSrc: str | None
        self.outerId: str | None
        self.gtin: str | None
        self.manufacturerPartNumber: str | None
        self.weightUnit: str | None
        self.weight: Decimal | None
        self.measureUnit: str | None
        self.height: Decimal | None
        self.width: Decimal | None
        self.length: Decimal | None
        self.brandName: str | None
        self.brand: BrandType | None
        self.masterVariation: VariationType | None
        self.variations: list[VariationType]
        self.hasVariations: bool
        self.availabilityData: AvailabilityData
        self.images: list[ImageType]
        self.price: PriceType
        self.prices: list[PriceType]
        self.minVariationPrice: PriceType | None
        self.properties: list[Property]
        self.keyProperties: list[Property]
        self.assets: list[Asset]
        self.outlines: list[OutlineType]
        self.breadcrumbs: list[Breadcrumb]
        self.vendor: CommonVendor | None
        self.rating: Rating | None
        self.inWishlist: bool
        self.wishlistIds: list[str]
        self.isPurchased: bool
        self.associations: ProductAssociationConnection | None
        self.videos: VideoConnection | None
