
import re

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
            "button",
            name="Submit",
            exact=True
        )

        # Locate the invalid-login error banner.
        self.login_error = self.page.get_by_text(
            "Having Trouble Logging In?",
            exact=False
        )

    def open_login_page(self):
        # Navigate to the GCT login page.
        self.navigate("https://www.gct.com/account/signin")

        # Wait for the initial page content.
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

            # Close the promotional popup.
            close_button.first.click()

            print("Promotional popup closed successfully!")

        else:
            print("Promotional popup is not displayed.")

    def enter_username(self, username):
        # Locate the username field.
        username_field = self.page.locator(self.username_field)

        # Activate the field.
        username_field.click()

        # Wait until the field is editable.
        expect(username_field).to_be_editable(timeout=10000)

        # Enter the username.
        username_field.fill(username)

        print("Username entered successfully!")

    def enter_password(self, password):
        # Locate the password field.
        password_field = self.page.locator(self.password_field)

        # Activate the field.
        password_field.click()

        # Wait until the field is editable.
        expect(password_field).to_be_editable(timeout=10000)

        # Enter the password.
        password_field.fill(password)

        print("Password entered successfully!")

    def click_submit(self):
        # Click the login Submit button.
        self.submit_button.click()

        print("Login Submit button clicked!")

    def is_login_error_displayed(self):
        # Wait for the error banner to appear.
        expect(self.login_error).to_be_visible(timeout=15000)

        # Read the complete visible page text.
        actual_text = self.page.locator("body").inner_text()

        # Normalize line breaks, tabs, and repeated spaces.
        normalized_text = re.sub(
            r"\s+",
            " ",
            actual_text
        ).strip().lower()

        # Check for the important invalid-login message.
        expected_text = "your username or password is incorrect"

        # Print the actual page text if verification fails.
        if expected_text not in normalized_text:
            print("Login error banner was found, but expected text was not matched.")
            print("Actual page text:")
            print(actual_text)
            return False

        print("Invalid login error message displayed successfully!")

        return True
