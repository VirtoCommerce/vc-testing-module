from PIL import Image
from io import BytesIO
from tests_visual.pages.login.login_page import LoginPage
from tests_visual.pages.registration.registration_page import RegistrationPage


def test_registration_public_visual(page, config, image_snapshot) -> None:
    """Test the registration page for visual consistency"""
    login = LoginPage(page, config)
    registration = RegistrationPage(page, config)

    # Navigate to login page
    login.navigate()

    # Click on the registration button
    login.click_registration_button()

    # Click on the nonprofit sector button
    registration.click_nonprofit_sector_button()

    # Freeze animations
    registration._freeze_animations()

    # Move cursor and take screenshot
    page.mouse.move(0, 0)
    page.wait_for_timeout(2000)

    image = Image.open(BytesIO(page.screenshot(full_page=True)))
    image_snapshot(
        image,
        "tests_visual/pages/registration/registration_snapshots/nonprofit/registration_nonprofit_base.png",
        threshold=0.4,
    )
