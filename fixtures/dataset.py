from typing import Any

import pytest

from dataset.dataset_manager import DatasetManager


@pytest.fixture(scope="session")
def dataset() -> dict[str, Any]:
    dataset_manager = DatasetManager()
    dataset_manager.load_requests()

    return dataset_manager.dataset
