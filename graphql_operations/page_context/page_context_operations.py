from typing import Optional
from gql import Client
from graphql_client.types.page_context_response_type import PageContextResponseType
from graphql_client.queries.page_context import PageContextQuery
from graphql_operations.page_context.fragments.page_context_fragment import PAGE_CONTEXT_FRAGMENT


class PageContextOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_page_context(
        self,
        store_id: Optional[str] = None,
        user_id: Optional[str] = None,
        culture_name: Optional[str] = None,
        domain: Optional[str] = None,
        permalink: Optional[str] = None,
        organization_id: Optional[str] = None,
        return_fields: Optional[str] = None,
    ) -> PageContextResponseType:
        page_context_query = PageContextQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "userId": user_id,
            "cultureName": culture_name,
            "domain": domain,
            "permalink": permalink,
            "organizationId": organization_id,
        }

        fields = return_fields if return_fields else PAGE_CONTEXT_FRAGMENT

        result = page_context_query.execute(variables=variables, return_fields=fields)

        return result

    def get_store_context(
        self,
        store_id: Optional[str] = None,
        culture_name: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> PageContextResponseType:
        """Get page context with only store-related fields"""
        return_fields = """
            store {
                storeId
                storeName
                catalogId
                storeUrl
                defaultCurrency {
                    code
                }
                defaultLanguage {
                    cultureName
                    nativeName
                    twoLetterLanguageName
                }
                availableLanguages {
                    cultureName
                    nativeName
                    twoLetterLanguageName
                }
                settings {
                    anonymousUsersAllowed
                }
            }
        """

        return self.get_page_context(
            store_id=store_id,
            culture_name=culture_name,
            domain=domain,
            return_fields=return_fields,
        )

    def get_slug_context(
        self,
        store_id: str,
        user_id: str,
        culture_name: str,
        permalink: str,
    ) -> PageContextResponseType:
        """Get page context with slug info fields"""
        return_fields = """
            slugInfo {
                entityInfo {
                    id
                    name
                    semanticUrl
                    pageTitle
                    metaDescription
                    imageAltDescription
                    metaKeywords
                    storeId
                    objectId
                    objectType
                    isActive
                    languageCode
                }
            }
        """

        return self.get_page_context(
            store_id=store_id,
            user_id=user_id,
            culture_name=culture_name,
            permalink=permalink,
            return_fields=return_fields,
        )

    def get_user_context(
        self,
        store_id: Optional[str] = None,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
    ) -> PageContextResponseType:
        """Get page context with user-related fields"""
        return_fields = """
            user {
                id
                memberId
                userName
                email
                emailConfirmed
                photoUrl
                phoneNumber
                permissions
                isAdministrator
                passwordExpired
                passwordExpiryInDays
                forcePasswordChange
                lockedState
                contact {
                    id
                    firstName
                    lastName
                    fullName
                    organizationId
                    defaultLanguage
                    currencyCode
                    selectedAddressId
                    organizations {
                        items {
                            id
                            name
                        }
                    }
                }
                operator {
                    userName
                    contact {
                        fullName             
                    }            
                }
                roles {
                    name
                }          
            }
        """

        return self.get_page_context(
            store_id=store_id,
            user_id=user_id,
            organization_id=organization_id,
            return_fields=return_fields,
        )

    def get_white_labeling_context(
        self,
        store_id: Optional[str] = None,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
    ) -> PageContextResponseType:
        """Get page context with white labeling settings"""
        return_fields = """
            whiteLabelingSettings {
                userId
                organizationId
                storeId
                logoUrl
                secondaryLogoUrl
                faviconUrl
                themePresetName
            }
        """

        return self.get_page_context(
            store_id=store_id,
            user_id=user_id,
            organization_id=organization_id,
            return_fields=return_fields,
        )

