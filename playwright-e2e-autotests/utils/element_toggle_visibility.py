def element_toggle_visibility(page, locator, hidden=True):
    """
    Toggle the visibility of an element on the page.

    Args:
        page: Playwright page instance.
        locator: CSS selector for the element.
        hidden (bool): Whether to hide or show the element. Defaults to True (hide).
    """
    visibility = "hidden" if hidden else "visible"
    page.add_style_tag(
        content=f"""
        {locator} {{
            visibility: {visibility};
        }}
    """
    )
