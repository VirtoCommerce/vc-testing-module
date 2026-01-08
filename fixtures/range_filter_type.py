import pytest
from pytest import FixtureRequest


@pytest.fixture
def range_filter_type(request: FixtureRequest) -> str:
    """Returns the range filter type (e.g., slider, default) specified via CLI."""
    return request.config.getoption("--range-filter-type")
