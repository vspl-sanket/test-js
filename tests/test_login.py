from __future__ import annotations

import re

from playwright.sync_api import expect


def _first_visible(page, locators):
    last_error = None
    for locator in locators:
        try:
            expect(locator).to_be_visible(timeout=5000)
            return locator
        except Exception as exc:  # pragma: no cover - fallback path
            last_error = exc
    raise AssertionError("Could not find a visible login field on the page.") from last_error


def _success_marker(page):
    candidates = [
        page.get_by_role("button", name=re.compile(r"^(log out|logout|sign out)$", re.I)),
        page.get_by_role("link", name=re.compile(r"^(log out|logout|sign out)$", re.I)),
        page.get_by_role("heading", name=re.compile(r"(dashboard|home|welcome)", re.I)),
        page.get_by_text(re.compile(r"(dashboard|welcome back|signed in)", re.I)),
    ]
    for locator in candidates:
        try:
            if locator.first.is_visible(timeout=2000):
                return locator.first
        except Exception:
            continue
    return None


def test_login_success(page, app_config):
    base_url = app_config["base_url"]

    page.goto(base_url, wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")

    username_field = _first_visible(
        page,
        [
            page.get_by_label(re.compile(r"^(username|email)$", re.I)),
            page.get_by_placeholder(re.compile(r"^(username|email)$", re.I)),
            page.locator('input[type="text"]'),
            page.locator('input[type="email"]'),
        ],
    )
    password_field = _first_visible(
        page,
        [
            page.get_by_label(re.compile(r"^password$", re.I)),
            page.get_by_placeholder(re.compile(r"^password$", re.I)),
            page.locator('input[type="password"]'),
        ],
    )

    username_field.fill(app_config["username"])
    password_field.fill(app_config["password"])

    login_button = _first_visible(
        page,
        [
            page.get_by_role("button", name=re.compile(r"^(log in|login|sign in)$", re.I)),
            page.get_by_role("link", name=re.compile(r"^(log in|login|sign in)$", re.I)),
            page.locator('button[type="submit"]'),
            page.locator('input[type="submit"]'),
        ],
    )

    login_button.click()
    page.wait_for_load_state("networkidle")

    success_marker = _success_marker(page)
    if success_marker is not None:
        expect(success_marker).to_be_visible(timeout=10000)
    else:
        expect(page).not_to_have_url(re.compile(r"(login|signin|sign-in)", re.I), timeout=10000)

    expect(username_field).not_to_be_visible(timeout=10000)
    expect(password_field).not_to_be_visible(timeout=10000)
