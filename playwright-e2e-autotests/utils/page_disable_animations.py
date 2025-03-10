def page_disable_animations(page):
    """
    Disable all animations and transitions on the page.

    Args:
        page: Playwright page instance.
    """
    page.add_style_tag(
        content="""
        * {
            animation: none !important;
            transition: none !important;
        }
    """
    )
