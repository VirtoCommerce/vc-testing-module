from PIL import Image
from io import BytesIO
from tests_visual.pages.homepage.homepage_page import HomePage
from tests_visual.pages.header.header_page import HeaderPage


def test_visual_homepage(authenticated_page, config, image_snapshot) -> None:
    page = authenticated_page
    header = HeaderPage(page)
    homepage = HomePage(page)

    page.wait_for_url(f"{config['base_url']}/home")
    page.wait_for_load_state("networkidle")

    header.hide_vc_badge()
    homepage.wait_for_product_images()

    page.mouse.move(0, 0)

    image = Image.open(BytesIO(page.screenshot(full_page=True)))
    image_snapshot(image, "tests_visual/pages/homepage/homepage_snapshots/homepage_base.png", True)
