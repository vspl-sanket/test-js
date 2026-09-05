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
BASE_URL=https://hc-uat.sysappai.net/
TEST_USERNAME=sanket_vspl
TEST_PASSWORD=Sanket123#
```

## Notes

- The test enters the username and fixed UAT verification code `12345`, submits `Proceed to Login`, then enters the password and submits `Log In`.
- The test uses the stable IDs and accessible button name from the UAT login page.
- Browser execution defaults to headless Chromium in CI. Use `pytest --browser chromium --headed -v` to watch the browser locally.
