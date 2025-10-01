import json
from typing import Any, Dict

import pytest


@pytest.fixture(scope="session")
def dataset() -> Dict[str, Any]:
    with open("dataset/dataset.json", "r", encoding="utf-8") as file:
        return json.load(file)
