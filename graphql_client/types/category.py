from pydantic import BaseModel


class Category(BaseModel):
    def __init__(self):
        from graphql_client.types.image_type import ImageType
        from graphql_client.types.property import Property
        from graphql_client.types.category_description_type import CategoryDescriptionType
        from graphql_client.types.category import Category
        from graphql_client.types.outline_type import OutlineType
        from graphql_client.types.seo_info import SeoInfo
        from graphql_client.types.breadcrumb import Breadcrumb
        from graphql_client.types.category_description_type import CategoryDescriptionType
        from graphql_client.types.category import Category

        self.id: str
        self.imgSrc: str | None
        self.code: str
        self.name: str
        self.level: int
        self.priority: int
        self.relevanceScore: float | None
        self.outline: str | None
        self.slug: str | None
        self.path: str | None
        self.seoInfo: SeoInfo
        self.descriptions: list[CategoryDescriptionType]
        self.description: CategoryDescriptionType | None
        self.parent: Category | None
        self.hasParent: bool
        self.outlines: list[OutlineType]
        self.images: list[ImageType]
        self.breadcrumbs: list[Breadcrumb]
        self.properties: list[Property]
        self.childCategories: list[Category]
