from graphql_operations.common.term_facets import TERM_FACETS_FRAGMENT


CART_PICKUP_LOCATION_FRAGMENT = f"""
    totalCount
    items {{
        id
        name
        description
        isActive
        contactEmail
        contactPhone
        workingHours
        geoLocation
        availabilityType
        availabilityNote
        availableQuantity
        address {{
            city
            countryCode
            countryName
            line1
            postalCode
            regionId
            regionName
        }}
    }}
    term_facets {{
        {TERM_FACETS_FRAGMENT}
    }}
"""