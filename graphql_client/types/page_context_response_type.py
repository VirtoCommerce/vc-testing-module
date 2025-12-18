from pydantic import BaseModel


class PageContextResponseType(BaseModel):
    def __init__(self):
        from graphql_client.types.user_type import UserType
        from graphql_client.types.white_labeling_settings_type import WhiteLabelingSettingsType
        from graphql_client.types.slug_info_response_type import SlugInfoResponseType
        from graphql_client.types.store_response_type import StoreResponseType

        self.slugInfo: SlugInfoResponseType | None
        self.store: StoreResponseType | None
        self.whiteLabelingSettings: WhiteLabelingSettingsType | None
        self.user: UserType | None
