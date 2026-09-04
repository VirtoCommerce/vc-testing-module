import os
from functools import cached_property
from pathlib import Path
from typing import Literal

from dotenv import dotenv_values
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).parent.parent / ".env"


class GlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILE, env_file_encoding="utf-8", extra="ignore")

    # Required
    frontend_base_url: str
    backend_base_url: str
    store_id: str
    admin_username: str
    admin_password: SecretStr
    users_password: SecretStr

    # Optional with defaults
    default_page_size: int = 50
    google_maps_api_key: SecretStr | None = None
    checkout_mode: Literal["single-page", "multi-step"] = "single-page"
    quantity_control: Literal["stepper", "button"] = "stepper"
    range_filter_type: Literal["slider", "default"] = "slider"
    page_builder_path: str = "/apps/page-builder-shell/?storeId={store_id}"
    requests_timeout: int = 30
    verify_ssl: bool = False
    poll_interval: int = 2
    poll_attempts: int = 10
    # Default timeout (ms) for Playwright actions, navigation, and web-first
    # assertions in e2e tests. Higher than Playwright's 5s assertion default so
    # tests tolerate slower remote environments (e.g. shared demo backends on
    # CI) where the UI settles later than it does against a local frontend.
    playwright_timeout: int = 30000

    def page_builder_shell_url(self, store_id: str | None = None, route: str | None = None) -> str:
        path = self.page_builder_path.format(store_id=store_id or self.store_id)
        url = f"{self.backend_base_url.rstrip('/')}/{path.lstrip('/')}"
        return f"{url}#/{route.lstrip('#/')}" if route else url

    @cached_property
    def env_vars(self) -> dict[str, str]:
        return {
            **{k: v for k, v in dotenv_values(_ENV_FILE).items() if v is not None},
            **os.environ,
        }


global_settings = GlobalSettings()  # type: ignore[call-arg]
