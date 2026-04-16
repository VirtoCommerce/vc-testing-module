from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class EntityDescriptor:
    name: str
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
    endpoint: str
    payload_type: Literal["single", "array"]
    priority: int = 99999
    data: list[dict[str, Any]] = field(default_factory=list)
