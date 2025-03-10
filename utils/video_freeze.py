def video_freeze(page):
    """
    Pause a video element on the page and set its current time to 1 second.
    This utility targets a specific video element using a hardcoded selector.

    Args:
        page: The Playwright page object.

    Returns:
        None
    """
    page.evaluate(
        """
        const video = document.querySelector('video');
        if (video) {
            video.pause();
            video.currentTime = 0; // Set to 0 second for consistency
        }
    """
    )
