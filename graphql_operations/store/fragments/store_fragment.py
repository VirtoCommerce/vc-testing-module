STORE_FRAGMENT = f"""
    storeId
    defaultCurrency {{
        code
    }}
    defaultLanguage {{
       cultureName
       nativeName
       twoLetterLanguageName
    }}
    availableLanguages {{
        cultureName
        nativeName
        twoLetterLanguageName
    }}
    settings {{
        anonymousUsersAllowed
    }}
"""
