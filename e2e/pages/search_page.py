from e2e.pages.locators.search_locators import SearchLocators
from playwright.sync_api import expect
from playwright.sync_api import Page
from playwright.sync_api import BrowserContext


class SearchPage:
    def __init__(self, page: Page, config: dict, browser_context: BrowserContext):
        self.page = page
        self.config = config
        self.browser_context = browser_context


    def search(self, query):
        expect(self.page.locator(SearchLocators.SEARCH_INPUT)).to_be_visible()
        self.page.locator(SearchLocators.SEARCH_INPUT).fill(query)
        self.page.wait_for_timeout(500)

    
    def verify_search_results(self, query):

        self.page.locator(SearchLocators.SEARCH_INPUT).fill(query)
        self.page.locator(SearchLocators.SEARCH_INPUT).press("Enter")
        self.page.wait_for_timeout(500)
        self.page.wait_for_selector(SearchLocators.DYNAMIC_SEARCH_POPUP, state="visible")
        expect(self.page.locator(SearchLocators.VIEW_ALL_RESULTS)).to_be_visible()
        self.page.locator(SearchLocators.VIEW_ALL_RESULTS).click()
        expect(self.page.locator(SearchLocators.SEARCH_TITLE)).to_be_visible()
        expect(self.page.locator(SearchLocators.SEARCH_TITLE)).to_contain_text(query)        
        text = self.page.locator(SearchLocators.SEARCH_RESULT_COUNT).text_content().strip()
        search_result_count = int(text)
        print(f"Search results count: {search_result_count}")
        assert search_result_count > 0, f"No search results found for query: {query}"






