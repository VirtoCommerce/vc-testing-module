import pytest
from pytest import FixtureRequest


@pytest.fixture
def checkout_mode(request: FixtureRequest):
    """Returns the checkout UI mode (e.g., single-page, multi-step) specified via CLI."""
    return request.config.getoption("--checkout-mode")
