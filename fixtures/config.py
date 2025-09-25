import os

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def config():
    load_dotenv(override=True)

    return {
        "backend_base_url": os.getenv("BACKEND_BASE_URL"),
        "frontend_base_url": os.getenv("FRONTEND_BASE_URL"),
        "store_id": os.getenv("STORE_ID"),
        "admin_username": os.getenv("ADMIN_USERNAME"),
        "admin_password": os.getenv("ADMIN_PASSWORD"),
        "users_password": os.getenv("USERS_PASSWORD"),
    }
