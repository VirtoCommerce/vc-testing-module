import os
from functools import cached_property
from pathlib import Path
from typing import Literal

from dotenv import dotenv_values
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).parent.parent / ".env"


class GlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE, env_file_encoding="utf-8", extra="ignore"
    )

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
    requests_timeout: int = 30
    verify_ssl: bool = False

    @cached_property
    def env_vars(self) -> dict[str, str]:
        return {
            **{k: v for k, v in dotenv_values(_ENV_FILE).items() if v is not None},
            **os.environ,
        }


global_settings = GlobalSettings()  # type: ignore[call-arg]
