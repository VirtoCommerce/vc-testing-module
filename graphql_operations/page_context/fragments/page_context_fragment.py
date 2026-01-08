PAGE_CONTEXT_FRAGMENT = """
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
    whiteLabelingSettings {
        userId
        organizationId
        storeId
        logoUrl
        secondaryLogoUrl
        faviconUrl
        themePresetName
    }
    user {
        id
        userName
        email
    }
"""

