import json

from playwright.sync_api import Page

from core.auth.token_info import TokenInfo


class BrowserStorage:
    _USER_ID_KEY = "user-id"
    _AUTH_KEY = "auth"

    def __init__(self, page: Page) -> None:
        self._page = page

    def get_user_id(self) -> str | None:
        return self._page.evaluate(f"localStorage.getItem('{self._USER_ID_KEY}')")

    def set_user_id(self, user_id: str) -> None:
        self._page.add_init_script(
            f"localStorage.setItem('{self._USER_ID_KEY}', '{user_id}')"
        )

    def set_auth(self, token_info: TokenInfo) -> None:
        expires_at = token_info.expires_at.isoformat(timespec="milliseconds").replace(
            "+00:00", "Z"
        )
        value = json.dumps({
            "expires_at": expires_at,
            "token_type": "Bearer",
            "access_token": token_info.access_token.get_secret_value(),
            "refresh_token": token_info.refresh_token,
        })
        self._page.add_init_script(
            f"localStorage.setItem('{self._AUTH_KEY}', {json.dumps(value)})"
        )
