from __future__ import annotations

import pytest

from config import BASE_URL, TEST_PASSWORD, TEST_USERNAME


@pytest.fixture(scope="session")
def app_config() -> dict[str, str]:
    if not TEST_USERNAME or not TEST_PASSWORD:
        pytest.fail("Set TEST_USERNAME and TEST_PASSWORD in .env before running the test.")

    return {
        "base_url": BASE_URL.rstrip("/"),
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args() -> dict[str, object]:
    return {
        "args": ["--disable-dev-shm-usage"],
        "chromium_sandbox": False,
    }
