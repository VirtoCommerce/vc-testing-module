import json
from typing import Any, Final, Protocol, runtime_checkable

from core.auth.platform_session import PlatformSession
from core.auth.provider import AuthProvider
from core.auth.token_info import TokenInfo

_EMPTY_STATE: Final[dict[str, Any]] = {"cookies": [], "origins": []}


@runtime_checkable
class BrowserAuth(Protocol):
    def storage_state(self) -> dict[str, Any]: ...


class AdminBrowserAuth:
    def __init__(self, session: PlatformSession) -> None:
        self._session = session

    def storage_state(self) -> dict[str, Any]:
        if not self._session.is_authenticated:
            return dict(_EMPTY_STATE)
        return self._session.storage_state()


class StorefrontBrowserAuth:
    _AUTH_KEY: Final = "auth"
    _USER_ID_KEY: Final = "user-id"

    def __init__(self, auth: AuthProvider, origin: str, user_id: str | None = None) -> None:
        self._auth = auth
        self._origin = origin.rstrip("/")
        self._user_id = user_id

    def storage_state(self) -> dict[str, Any]:
        items: list[dict[str, str]] = []
        token_info = self._auth.token_info
        if token_info is not None:
            items.append({"name": self._AUTH_KEY, "value": _serialize_token(token_info)})
        if self._user_id is not None:
            items.append({"name": self._USER_ID_KEY, "value": self._user_id})
        if not items:
            return {"cookies": [], "origins": []}
        return {
            "cookies": [],
            "origins": [{"origin": self._origin, "localStorage": items}],
        }


def merge_storage_states(*states: dict[str, Any]) -> dict[str, Any]:
    cookies: list[dict[str, Any]] = []
    origins: dict[str, dict[str, str]] = {}
    for state in states:
        cookies.extend(state.get("cookies") or [])
        for entry in state.get("origins") or []:
            bucket = origins.setdefault(entry["origin"], {})
            for item in entry.get("localStorage") or []:
                bucket[item["name"]] = item["value"]
    return {
        "cookies": cookies,
        "origins": [
            {
                "origin": origin,
                "localStorage": [{"name": k, "value": v} for k, v in items.items()],
            }
            for origin, items in origins.items()
        ],
    }


def _serialize_token(token_info: TokenInfo) -> str:
    expires_at = token_info.expires_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return json.dumps(
        {
            "expires_at": expires_at,
            "token_type": "Bearer",
            "access_token": token_info.access_token.get_secret_value(),
            "refresh_token": token_info.refresh_token,
        }
    )
