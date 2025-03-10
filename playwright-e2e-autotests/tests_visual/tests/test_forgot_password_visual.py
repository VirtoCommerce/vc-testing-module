from PIL import Image
from io import BytesIO
from tests_visual.pages.forgot_password.forgot_password_page import ForgotPasswordPage


def test_forgot_password_visual(page, config, image_snapshot) -> None:
    """Test the forgot password page for visual consistency"""
    forgot_password = ForgotPasswordPage(page, config)

    # Navigate to forgot password page
    forgot_password.navigate()

    # Move cursor and take screenshot
    page.mouse.move(0, 0)
    page.wait_for_timeout(2000)

    image = Image.open(BytesIO(page.screenshot(full_page=True)))
    image_snapshot(
        image,
        "tests_visual/pages/forgot_password/forgot_password_snapshots/forgot_password_base.png",
        threshold=0.4,
    )
