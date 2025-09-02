# Description
Dataset prompt for electronics store "ACME"
- store name should be used in all generated data as part of a store name, catalog name, etc., e.g., "ACME Electronics Store", "ACME Electronics Catalog"
- domain name: acme.com
- all IDs in data schema should be UUIDs

# Goal
- Generate languages: en-US, de-DE
- Generate currencies: USD, EUR, GBP
- Generate 5 fulfillment centers in different countries
- Generate catalog with 2 languages: en-US, de-DE; en-US is default
- Generate catalog property groups: Processor, Memory, Storage, Display
- Generate store with 2 languages: en-US, de-DE (default: en-US); 3 currencies: USD, EUR, GBP (default: USD); all fulfillment centers (take a random as default)
- Generate pricelist with currencies: USD, EUR, GBP
- Generate pricelists assignments for all currencies
- Generate category tree:
    - Laptops
        - Laptops for home and office
        - Laptops for gaming
        - Laptops for professionals
- Generate category properties only for Laptops category:
    - Processor (group)
        - Processor Max Frequency (in GHz)
        - Processor Cores Number
        - Processor Model (e.g. Intel Core i5-12400F)
        - Processor Threads Number
    - Memory (group)
        - Memory Size (in GB)
        - Memory Type (e.g. DDR5)
        - Memory Speed (in MHz)
        - Memory Slots Number (e.g. 2)
    - Storage (group)
        - Storage Size (in GB)
        - Storage Type (e.g. M.2 NVMe)
    - Display (group)
        - Display Size (in inches)
        - Display Type (e.g. OLED)
        - Display Resolution (e.g. 1920x1080)
        - Display Refresh Rate (in Hz)
    - Battery Capacity (in mAh)
    - Keyboard Backlight (Boolean)

---

# Data Schema

### Currencies
- Fields:
    - `code` (3-letters currency code)
    - `name` (currency name)
- Examples: "USD" (name: "US Dollar"), "EUR" (name: "Euro")

### Languages
- string array of culture names in languagecode2-country/regioncode2 format
- Examples: "en-US", "de-DE"


### Fulfillment Centers
- Fields:
    - `id`
    - `name` (FFC name in format {country/region name} FFC")
    - `address`
        - `addressType` (always "Shipping")
        - `city`
        - `countryCode` (3-letters country code)
        - `countryName` (full country name, e.g "United States of America")
        - `line1`
        - `postalCode`
        - `regionCode` (2-letters region code if it exists for country)
        - `regionName` (if it exists for country)
        - `email` (FFC name in kebab-case)
        - `phone` (phone number for country/region)

### Catalogs
- Fields:
    - `id`
    - `name`
    - `languages`
        - `languageCode` (culture names in languagecode2-country/regioncode2 format)
        - `isActive` (true)
        - `isDefault`

### Catalog Property Groups
- Fields:
    - `id`
    - `catalogId`
    - `name`
    - `localizedName`
        - `values`
            - culture name in languagecode2-country/regioncode2 format as key
            - string value

### Stores
- Fields:
    - `id`
    - `name`
    - `catalog` (catalog ID)
    - `storeState` ("Open")
    - `defaultCurrency` (3-letters currency code)
    - `defaultLanguage` (culture name in languagecode2-country/regioncode2 format)
    - `mainFulfillmentCenterId`
    - `currencies` (string array of codes of all currencies except of default currency)
    - `languages` (string array of all languages except of default language)
    - `additionalFulfillmentCenters` (string array of IDs of all fulfillment centers except of main fulfillment center ID)

### Pricelists
- Fields:
    - `id`
    - `name`
    - `currency` (3-letters currency code)

### Pricelists Assignments
- Fields:
    - `catalogId`
    - `pricelistId`
    - `name`

### Categories
- Fields:
    - `id`
    - `code` (lowercased kebab-case category name)
    - `catalogId`
    - `parentId` (id of parent category, exclude field for top-level category)
    - `name`
    - `seoObjectType` ("Category")

### Category Properties
- Fields
    - `id`
    - `catalogId`
    - `categoryId`
    - `propertyGroupId` (exclude field if not needed)
    - `name` (property name in pascal-case, e.g. ProcessorMaxFrequency)
    - `type` ("Product" for all category products)
    - `valueType` ("ShortText" by default)
    - `displayNames`
        - `languageCode`
        - `name` (localized display name)

# Products
- Fields:
    - `id`
    - `catalogId`
    - `categoryId`
    - `name`
    - `code` (product SKU, lowercased kebeb-case product name)
    - `vendor`
    - `productType` ("Physical" or "Digital")
    - `weightUnit`
    - `measureUnit`
    - `weight` (float, e.g. 1.63)
    - `width` (int)
    - `height` (int)
    - `length` (int)
    - `properties`