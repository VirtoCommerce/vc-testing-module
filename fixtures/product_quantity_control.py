import pytest
from pytest import FixtureRequest


@pytest.fixture
def product_quantity_control(request: FixtureRequest) -> str:
    """Returns the quantity selector style (e.g., stepper, button) specified via CLI."""
    return request.config.getoption("--product-quantity-control")
