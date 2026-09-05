from playwright.sync_api import expect


def test_login_success(page, app_config):
    page.goto(app_config["base_url"], wait_until="domcontentloaded")

    page.locator("#usercaptcha-user_name").fill(app_config["username"])
    page.locator("#usercaptcha-verifycode").fill("12345")
    page.locator("#login-button").click()

    password_page = page.locator("form.auth-form-box")
    expect(password_page).to_be_visible(timeout=10000)
    expect(page.locator("#user_pass")).to_be_visible(timeout=10000)

    password_page_url = page.url
    page.locator("#user_pass").fill(app_config["password"])
    page.get_by_role("button", name="Log In").click()

    page.wait_for_load_state("networkidle")
    expect(page.locator("#user_pass")).not_to_be_visible(timeout=10000)
    expect(page).not_to_have_url(password_page_url, timeout=10000)
