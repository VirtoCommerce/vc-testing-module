def element_mock_text(page, locator, replacement="mocked text"):
    """
    Modify the text content for all elements matched by the given locator.

    :param page: Playwright page object
    :param locator: CSS selector for the element to modify
    :param replacement: The text to set for the matched elements (default is "mocked text").
    """
    page.locator(locator).evaluate_all(
        f"""elements => {{
            elements.forEach(element => {{
                element.textContent = "{replacement}";
            }});
        }}"""
    )
