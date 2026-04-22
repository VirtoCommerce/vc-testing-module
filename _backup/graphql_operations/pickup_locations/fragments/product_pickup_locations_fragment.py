PRODUCT_PICKUP_LOCATION_FRAGMENT = """
    totalCount
    items {
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
        address {
            city
            countryCode
            countryName
            line1
            postalCode
            regionId
            regionName
        }
    }
"""
