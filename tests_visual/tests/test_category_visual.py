from PIL import Image
from io import BytesIO
from tests_visual.pages.category.category_page import CategoryPage
from tests_visual.pages.header.header_page import HeaderPage
from utils.force_image_loading import force_image_loading


def test_visual_category(authenticated_page, config, image_snapshot) -> None:
    page = authenticated_page
    header = HeaderPage(page)
    category = CategoryPage(page, config)

    # Navigate to category page
    category.navigate()

    # Force image loading
    force_image_loading(page)
    header.hide_vc_badge()

    # Mock results count
    category.mock_results_count()
    category.wait_for_product_images()

    # Take a screenshot
    page.mouse.move(0, 0)
    image = Image.open(BytesIO(page.screenshot(full_page=True)))
    image_snapshot(image, "tests_visual/pages/category/category_snapshots/category_base.png", True)
