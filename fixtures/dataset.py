import json
from datetime import datetime
from typing import Any, Dict

import pytest

from dataset.dataset_manager import DatasetManager


@pytest.fixture(scope="session")
def dataset() -> Dict[str, Any]:
    dataset_manager = DatasetManager()
    dataset_manager.load_requests()

    with open("dataset/dataset.json", "w", encoding="utf-8") as file:
        json.dump(dataset_manager.dataset, file, indent=4)

    return dataset_manager.dataset
