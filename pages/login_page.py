
from pages.base_page import BasePage
from playwright.sync_api import expect


class LoginPage(BasePage):

    def __init__(self, page):
        # Initialize common browser methods from BasePage.
        super().__init__(page)

        # Stable locators for username and password fields.
        self.username_field = "input[name='signin-username']"
        self.password_field = "input[name='signin-password']"

        # Locator for the promotional popup close button.
        self.promo_close_button = (
            "form#WebPop button:has(span.icon-close-rounded)"
        )

        # Locator for the login Submit button.
        self.submit_button = self.page.get_by_role(
            "button", name="Submit", exact=True
        )

        # Expected error message for invalid login credentials.
        self.login_error = self.page.get_by_text(
            "Your username or password is incorrect.",
            exact=False
        )

    def open_login_page(self):
        # Navigate to the GCT login page.
        self.navigate("https://www.gct.com/account/signin")

        # Wait until the initial page content loads.
        self.page.wait_for_load_state("domcontentloaded")

        # Close the promotional popup if it appears.
        self.close_promo_popup()

        # Accept cookies if the consent popup appears.
        self.accept_cookies()

        print("Login page opened and popups handled!")

    def close_promo_popup(self):
        # Locate the close button inside the promotional popup.
        close_button = self.page.locator(
            self.promo_close_button
        )

        # Check whether the popup exists and is visible.
        if close_button.count() > 0 and close_button.first.is_visible():

            # Click the close button.
            close_button.first.click()

            print("Promotional popup closed successfully!")

        else:
            print("Promotional popup is not displayed.")

    def enter_username(self, username):
        # Locate the username field.
        username_field = self.page.locator(self.username_field)

        # Click the field to activate it.
        username_field.click()

        # Wait until the field becomes editable.
        expect(username_field).to_be_editable(timeout=10000)

        # Enter the username.
        username_field.fill(username)

        print("Username entered successfully!")

    def enter_password(self, password):
        # Locate the password field.
        password_field = self.page.locator(self.password_field)

        # Click the field to activate it.
        password_field.click()

        # Wait until the field becomes editable.
        expect(password_field).to_be_editable(timeout=10000)

        # Enter the password.
        password_field.fill(password)

        print("Password entered successfully!")

    def click_submit(self):
        # Click the login Submit button.
        self.submit_button.click()

    def is_login_error_displayed(self):
        # Wait for the invalid-login error message.
        self.login_error.wait_for(
            state="visible",
            timeout=10000
        )

        # Return True if the error message is visible.
        return self.login_error.is_visible()
