class SearchLocators:
    SEARCH_INPUT = "//input[@type='search']"
    SEARCH_TITLE = "//span[contains(.,'Your search for {} returned the following')]"
    SEARCH_RESULTS = "//div[@class='vc-product-card__title']"
    SEARCH_RESULT_COUNT = "//sup[@class='category__products-count']/b" 
    VIEW_ALL_RESULTS = "(//button[contains(.,'View all')])[1]"
    DYNAMIC_SEARCH_POPUP = "//div[contains(@class,'absolute left-1/2')]"

