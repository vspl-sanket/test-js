# SysApp UAT Login Test

Minimal Playwright + Pytest project for validating only the SysApp UAT login flow.

## Structure

```text
.
├── .env
├── .env.example
├── .gitignore
├── conftest.py
├── config.py
├── pytest.ini
├── requirements.txt
└── tests/
    └── test_login.py
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

## Run

Run the login test:

```bash
pytest -v
```

Generate an HTML report:

```bash
pytest --html=report.html --self-contained-html
```

## Environment

Copy `.env.example` to `.env` and keep the credentials there.

```ini
BASE_URL=https://uat.sysappai.net/
TEST_USERNAME=sanket_vspl
TEST_PASSWORD=Sanket123#
```

## Notes

- The test uses Playwright role/label-based locators first, with a small fallback chain for common login form variants.
- Browser execution is configured for headless Chromium so it works in CI.
