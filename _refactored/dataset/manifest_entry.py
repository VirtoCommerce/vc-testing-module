from dataclasses import dataclass
from typing import Literal


@dataclass
class ManifestEntry:
    name: str
    module_id: str
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
    endpoint: str
    payload_type: Literal["single", "array"]
