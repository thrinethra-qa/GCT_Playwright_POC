
from pages.base_page import BasePage
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError


class SignupPage(BasePage):

    def __init__(self, page):
        # Initialize common browser methods from BasePage.
        super().__init__(page)

        # Locator for the Email Address input field.
        self.email_field = "input[id='_R_49f5fivdb_']"

        # Locator for the Enter button.
        self.enter_button = self.page.get_by_role(
            "button",
            name="Enter",
            exact=True
        )

        # Locator for the empty email validation message.
        self.email_required_error = self.page.get_by_text(
            "Email address is required",
            exact=True
        )

        # Locator for a dialog that may block the page.
        self.blocking_dialog = self.page.locator('[role="dialog"]')

    def open_registration_lookup_page(self):
        # Open the GCT Registration Lookup page.
        self.navigate("https://www.gct.com/account/lookup")

        # Wait until the initial page content loads.
        self.page.wait_for_load_state("domcontentloaded")

        # Accept cookies if the consent popup appears.
        self.accept_cookies()

        # Close the promotional popup if it appears.
        self.close_promo_popup()

        print("Registration Lookup page opened successfully!")

    def dismiss_blocking_dialog(self):
        # Check whether a dialog is currently visible.
        try:
            self.blocking_dialog.first.wait_for(
                state="visible",
                timeout=1500
            )

            # Press Escape to dismiss a dismissible Radix dialog.
            self.page.keyboard.press("Escape")

            # Wait briefly for the dialog to close.
            self.blocking_dialog.first.wait_for(
                state="hidden",
                timeout=5000
            )

            print("Blocking dialog dismissed successfully!")

        except PlaywrightTimeoutError:
            # Continue if no visible dialog is present.
            print("No blocking dialog was displayed.")

    def verify_email_required_error(self):
        # Dismiss any dialog that may intercept the field click.
        self.dismiss_blocking_dialog()

        # Locate the email input field.
        email_field = self.page.locator(self.email_field)

        # Wait until the email field is visible and ready.
        expect(email_field).to_be_visible(timeout=15000)
        expect(email_field).to_be_enabled(timeout=10000)

        # Click the empty field to give it focus.
        email_field.click(timeout=10000)

        # Press Tab to trigger field validation.
        email_field.press("Tab")

        # Wait for the required email message to appear.
        expect(self.email_required_error).to_be_visible(
            timeout=10000
        )

        print("Email required validation message displayed!")

    def verify_enter_button_disabled(self):
        # Verify that the Enter button cannot be clicked
        # while the email field is empty.
        expect(self.enter_button).to_be_disabled(
            timeout=10000
        )

        print("Enter button is disabled for an empty email field!")
