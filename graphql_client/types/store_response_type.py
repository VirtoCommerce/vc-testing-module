from pydantic import BaseModel


class StoreResponseType(BaseModel):
    def __init__(self):
        from graphql_client.types.language_type import LanguageType
        from graphql_client.types.graph_ql_settings_type import GraphQLSettingsType
        from graphql_client.types.language_type import LanguageType
        from graphql_client.types.currency_type import CurrencyType
        from graphql_client.types.store_settings_type import StoreSettingsType
        from graphql_client.types.currency_type import CurrencyType

        self.storeId: str
        self.storeName: str
        self.catalogId: str
        self.storeUrl: str | None
        self.defaultLanguage: LanguageType
        self.availableLanguages: list[LanguageType]
        self.defaultCurrency: CurrencyType
        self.availableCurrencies: list[CurrencyType]
        self.settings: StoreSettingsType
        self.graphQLSettings: GraphQLSettingsType
