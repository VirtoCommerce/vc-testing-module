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
        "test_customer_username": os.getenv("TEST_CUSTOMER_USERNAME"),
        "test_customer_password": os.getenv("TEST_CUSTOMER_PASSWORD"),
        "test_permanent_customer_username": os.getenv(
            "TEST_PERMANENT_CUSTOMER_USERNAME"
        ),
        "test_permanent_customer_password": os.getenv(
            "TEST_PERMANENT_CUSTOMER_PASSWORD"
        ),
        "test_permanent_corporate_customer_username": os.getenv(
            "TEST_PERMANENT_CORPORATE_CUSTOMER_USERNAME"
        ),
        "test_permanent_corporate_customer_password": os.getenv(
            "TEST_PERMANENT_CORPORATE_CUSTOMER_PASSWORD"
        ),
        "test_admin_username": os.getenv("TEST_ADMIN_USERNAME"),
        "test_admin_password": os.getenv("TEST_ADMIN_PASSWORD"),
    }
