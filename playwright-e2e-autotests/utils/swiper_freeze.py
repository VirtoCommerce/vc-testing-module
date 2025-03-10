def swiper_freeze(page, locator):
    """
    Freeze the swiper element's animations, stop autoplay, and disable interactions.
    This utility targets a specific swiper element passed via the selector argument.

    Args:
        page: The Playwright page object.
        locator: A string representing the selector for the swiper element.

    Returns:
        None
    """
    page.evaluate(
        f"""
        const swiper = document.querySelector('{locator}');
        if (swiper && swiper.swiper) {{
            // Stop autoplay if enabled
            swiper.swiper.autoplay?.stop();

            // Move to a specific slide (e.g., first slide)
            swiper.swiper.slideTo(0, 0); // 0ms transition to ensure instant stop

            // Disable all interactions
            swiper.swiper.disable();
        }}
    """
    )
