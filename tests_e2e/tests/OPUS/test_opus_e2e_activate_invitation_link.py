import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from tests_e2e.components.greetings_popup_component import GreetingsPopupComponent
from tests_e2e.pages.home_page import HomePage
from utils.generate_invitation_link_opus_registration import (
    generate_invitation_link_opus_registration,
)


@pytest.mark.e2e
@allure.feature("Activate Invitation Link and Verify Greetings Popup (E2E)")
def test_opus_e2e_activate_invitation_link(config: dict[str, Any], page: Page):
    """
    Test activating an invitation link and verifying the greetings popup elements.
    
    This test:
    1. Generates an invitation link via the opus-registration API
    2. Visits the invitation link
    3. Verifies the URL redirects to /home
    4. Verifies all greetings popup elements are displayed correctly
    """
    print(f"{os.linesep}{'='*80}")
    print("Running E2E test to activate invitation link and verify greetings popup...")
    print('='*80)

    # Generate the invitation link
    print(f"{os.linesep}Step 1: Generating invitation link via Opus Registration API...")
    invitation_link = generate_invitation_link_opus_registration(
        config=config,
        first_name="E2E",
        last_name="Test",
        organization_name="E2E Test Organization",
    )
    
    print(f"{os.linesep}✅ Invitation link generated: {invitation_link}")

    # Visit the invitation link
    print(f"{os.linesep}Step 2: Visiting the invitation link...")
    page.goto(invitation_link)
    page.wait_for_load_state("networkidle")

    # Verify the URL redirects to /home
    home_page = HomePage(page, config)
    print(f"{os.linesep}Step 3: Verifying URL redirects to /home...")
    expect(page).to_have_url(home_page.url)
    print(f"{os.linesep}✅ URL verified: {page.url}")

    # Initialize the greetings popup component
    greetings_popup = GreetingsPopupComponent(page)

    # Verify all greetings popup elements
    print(f"{os.linesep}Step 4: Verifying greetings popup elements...")
    
    print(f"{os.linesep}  - Checking welcome header...")
    greetings_popup.get_welcome_header()
    
    print(f"{os.linesep}  - Checking Opus logo...")
    greetings_popup.get_opus_logo()
    
    print(f"{os.linesep}  - Checking 'We are processing' text...")
    greetings_popup.get_we_are_processing_text()
    
    print(f"{os.linesep}  - Checking 'You will receive an email' text...")
    greetings_popup.get_you_will_receive_an_email_text()
    
    print(f"{os.linesep}  - Checking 'In the meantime' text...")
    greetings_popup.get_in_the_mean_time_text()
    
    print(f"{os.linesep}  - Checking first point mark...")
    greetings_popup.get_first_point_mark()
    
    print(f"{os.linesep}  - Checking 'Research and buy' text...")
    greetings_popup.get_research_and_buy_text()
    
    print(f"{os.linesep}  - Checking 'Take a tour' button...")
    greetings_popup.get_take_a_tour_button()
    
    print(f"{os.linesep}  - Checking 'Start exploring' button...")
    greetings_popup.get_start_exploring_button()
    
    print(f"{os.linesep}  - Checking second point mark...")
    greetings_popup.get_second_point_mark()
    
    print(f"{os.linesep}  - Checking 'Explore the entire OMNIA' text...")
    greetings_popup.get_explore_the_entire_omnia_text()
    
    print(f"{os.linesep}  - Checking portfolio link...")
    greetings_popup.get_portfolio_link()
    
    print(f"{os.linesep}  - Checking close button...")
    greetings_popup.get_close_button()

    print(f"{os.linesep}{'='*80}")
    print("✅ All greetings popup elements verified successfully!")
    print('='*80)

