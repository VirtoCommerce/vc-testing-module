from PIL import Image
from io import BytesIO
from tests_visual.pages.login.login_page import LoginPage
from tests_visual.pages.registration.registration_page import RegistrationPage


def test_registration_company_visual(page, config, image_snapshot) -> None:
    """Test the registration page for visual consistency"""
    login = LoginPage(page, config)
    registration = RegistrationPage(page, config)

    # Navigate to login page
    login.navigate()

    # Click on the registration button
    login.click_registration_button()

    # Move cursor and take screenshot
    page.mouse.move(0, 0)
    page.wait_for_timeout(2000)

    image = Image.open(BytesIO(page.screenshot(full_page=True)))
    image_snapshot(
        image,
        "tests_visual/pages/registration/registration_snapshots/company_account/registration_company_account.png",
        threshold=0.4,
    )
