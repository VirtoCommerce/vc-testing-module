def element_replace_numbers_in_text(page, locator, replacement="888"):
    """
    Replace all numbers in the text content of an element with a specified value.

    Args:
        page: Playwright page instance.
        locator: Locator object or string to identify the target element.
        replacement: The string to replace numbers with (default is "888").
    """
    # Check if locator is a string and convert it to a Locator object
    if isinstance(locator, str):
        locator = page.locator(locator)

    locator.evaluate(
        f"""
        element => {{
            element.textContent = element.textContent.replace(/\\d+/g, "{replacement}");
        }}
        """
    )
