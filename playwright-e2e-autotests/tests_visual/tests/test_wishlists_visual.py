from PIL import Image
from io import BytesIO
from tests_visual.pages.wishlists.wishlists_page import WishlistsPage
from tests_visual.pages.header.header_page import HeaderPage


def test_visual_wishlists(authenticated_page, config, image_snapshot) -> None:
    page = authenticated_page
    header = HeaderPage(page)
    wishlists = WishlistsPage(page, config)

    # Navigate to wishlists page
    wishlists.navigate()
    header.hide_vc_badge()

    # Move mouse to top left corner
    page.mouse.move(0, 0)

    # Take screenshot
    image = Image.open(BytesIO(page.screenshot(full_page=True)))
    image_snapshot(
        image,
        "tests_visual/pages/wishlists/wishlists_snapshots/wishlists_base.png",
        True,
    )
