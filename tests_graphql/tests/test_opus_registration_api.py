import os
from typing import Any

import allure
import pytest

from utils.generate_invitation_link_opus_registration import (
    generate_invitation_link_opus_registration,
)


@pytest.mark.graphql
@allure.feature("Generate Invitation Link via Opus Registration API")
def test_opus_registration_api(
    config: dict[str, Any],
):
    """
    Test the generate_invitation_link_opus_registration utility function.
    
    This test:
    1. Calls the /api/v1/opus-registration API
    2. Generates an invitation link
    3. Prints the link to console
    4. Verifies the link format
    """
    print(f"{os.linesep}{'='*80}")
    print("Testing Opus Registration API...")
    print('='*80)

    # Call the utility function
    invitation_link = generate_invitation_link_opus_registration(
        config=config,
        first_name="Test",
        last_name="User",
        organization_name="Test Organization API",
    )

    # Print the invitation link prominently
    print(f"{os.linesep}{'='*80}")
    print("✅ INVITATION LINK GENERATED SUCCESSFULLY!")
    print('='*80)
    print(f"{invitation_link}")
    print('='*80)

    # Verify the invitation link format
    assert invitation_link is not None, "Invitation link should not be None"
    assert invitation_link != "", "Invitation link should not be empty"
    assert invitation_link.startswith("http"), "Invitation link should be a valid URL"
    
    print(f"{os.linesep}✓ Opus Registration API test passed!")

