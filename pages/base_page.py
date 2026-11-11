
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class BasePage:

    def __init__(self, page):
        # Store the Playwright page so all page classes can use it.
        self.page = page

    def navigate(self, url):
        # Open the requested URL.
        self.page.goto(url)

    def click(self, locator):
        # Click an element using its locator.
        self.page.locator(locator).click()

    def fill(self, locator, value):
        # Enter text into an input field.
        self.page.locator(locator).fill(value)

    def get_text(self, locator):
        # Return the text displayed by an element.
        return self.page.locator(locator).inner_text()

    def is_visible(self, locator):
        # Check whether an element is visible.
        return self.page.locator(locator).is_visible()

    def go_back(self):
        # Navigate to the previous browser page.
        self.page.go_back()

    def go_forward(self):
        # Navigate to the next browser page.
        self.page.go_forward()

    def accept_cookies(self):
        # Locate the cookie consent dialog.
        cookie_popup = self.page.get_by_role(
            "dialog",
            name="Cookie consent"
        )

        try:
            # Wait up to 5 seconds for the cookie popup to appear.
            cookie_popup.wait_for(
                state="visible",
                timeout=5000
            )

            # Locate the Accept button inside the cookie dialog.
            accept_button = cookie_popup.get_by_role(
                "button",
                name="Accept",
                exact=True
            )

            # Click the Accept button.
            accept_button.click()

            # Wait until the cookie popup disappears.
            cookie_popup.wait_for(
                state="hidden",
                timeout=5000
            )

            print("Cookie consent accepted successfully!")

        except PlaywrightTimeoutError:
            # Continue if the cookie popup does not appear.
            print("Cookie consent popup was not displayed.")

    def close_promo_popup(self):
        # Locate the close button inside the promotional popup.
        promo_close_button = self.page.locator(
            "form#WebPop button:has(span.icon-close-rounded)"
        )

        try:
            # Wait up to 5 seconds for the close button to appear.
            promo_close_button.wait_for(
                state="visible",
                timeout=5000
            )

            # Click the promotional popup close button.
            promo_close_button.click()

            # Verify that the popup has disappeared.
            promo_close_button.wait_for(
                state="hidden",
                timeout=5000
            )

            print("Promotional popup closed successfully!")

        except PlaywrightTimeoutError:
            # Continue if the promotional popup is not displayed.
            print("Promotional popup was not displayed!")
