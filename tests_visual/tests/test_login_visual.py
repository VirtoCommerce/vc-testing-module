from PIL import Image
from io import BytesIO
from tests_visual.pages.login.login_page import LoginPage


def test_visual_login(page, config, image_snapshot) -> None:
    """Test the login page for visual consistency"""
    login = LoginPage(page, config)

    # Navigate and freeze animations
    login.navigate()
    page.pause()

    # Move cursor and take screenshot
    page.mouse.move(0, 0)
    page.wait_for_timeout(2000)

    image = Image.open(BytesIO(page.screenshot(full_page=True)))
    image_snapshot(image, "tests_visual/pages/login/login_snapshots/login_base.png", threshold=0.4)
