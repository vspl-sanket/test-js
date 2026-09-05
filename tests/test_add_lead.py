from __future__ import annotations

from playwright.sync_api import expect


FIRST_NAME = "sankettest"
LAST_NAME = "purohittest"
SALES_PERSON = "Mahima"
DISPOSITION = "Attempting Contact - PURL"


def _login(page, app_config) -> None:
    page.goto(app_config["base_url"], wait_until="domcontentloaded")

    page.locator("#usercaptcha-user_name").fill(app_config["username"])
    page.locator("#usercaptcha-verifycode").fill("12345")
    page.locator("#login-button").click()

    password_page = page.locator("form.auth-form-box")
    expect(password_page).to_be_visible(timeout=10000)
    expect(page.locator("#user_pass")).to_be_visible(timeout=10000)

    page.locator("#user_pass").fill(app_config["password"])
    page.get_by_role("button", name="Log In").click()

    page.wait_for_load_state("networkidle")
    expect(page.locator("#user_pass")).not_to_be_visible(timeout=10000)
    expected_home_url = f'{app_config["base_url"]}/main/home'
    expect(page).to_have_url(expected_home_url, timeout=15000)


def _open_add_lead(page) -> None:
    sales_menu = page.locator('a[href="#nv-mnuSales"]')
    expect(sales_menu).to_be_visible(timeout=10000)
    sales_menu.click()

    expect(sales_menu).to_have_attribute("aria-expanded", "true", timeout=10000)
    add_lead = page.locator('#nv-mnuSales a[menu-id="12"]')
    add_lead.wait_for(state="visible", timeout=10000)
    add_lead.click()

    expect(page.get_by_text("Add Lead", exact=True)).to_be_visible(timeout=15000)


def _fill_text_field(page, label: str, value: str) -> None:
    groups = page.locator("div.bo-form-group").filter(has_text=label)
    groups = groups.filter(has=page.locator("input"))
    field = groups.first.locator("input").first
    expect(field).to_be_visible(timeout=10000)
    field.fill(value)


def _select_field_option(page, label: str, option_text: str) -> None:
    groups = page.locator(f'div.bo-form-group:has(h5:text-is("{label}"))')
    if groups.count() == 0:
        groups = page.locator(f'div.bo-form-group:has-text("{label}")')
    group = groups.first

    combobox = group.locator('[role="combobox"], .select2-selection').first
    if combobox.count() > 0:
        with page.expect_response(
            lambda response: "lookup" in response.url,
            timeout=10000,
        ):
            combobox.click()

        option = page.get_by_role("option", name=option_text, exact=True)
        expect(option).to_be_visible(timeout=10000)
        option.click()
        return

    select = group.locator("select").first
    if select.count() > 0:
        select.select_option(label=option_text)
        return

    raise AssertionError(f"Could not find a selectable control for {label!r}.")


def _assert_no_validation_errors(page) -> None:
    validation_box = page.locator("#bo-form-div-brule")
    if validation_box.is_visible():
        messages = validation_box.locator("#bo-form-brule li").all_inner_texts()
        raise AssertionError(
            "Lead save was blocked by validation errors: " + "; ".join(messages)
        )


def test_login_and_create_add_lead(page, app_config):
    _login(page, app_config)
    _open_add_lead(page)

    _fill_text_field(page, "First Name", FIRST_NAME)
    _fill_text_field(page, "Last Name", LAST_NAME)
    _select_field_option(page, "Salesperson", SALES_PERSON)
    _select_field_option(page, "Disposition", DISPOSITION)

    page.locator("#btnSave").click()
    page.wait_for_timeout(1500)
    _assert_no_validation_errors(page)
