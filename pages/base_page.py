from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
class BasePage:

    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def click(self, locator):
        self.page.locator(locator).click()

    def fill(self, locator, value):
        self.page.locator(locator).fill(value)

    def get_text(self, locator):
        return self.page.locator(locator).inner_text()

    def is_visible(self, locator):
        return self.page.locator(locator).is_visible()

    def go_back(self):
        self.page.go_back()

    def go_forward(self):
        self.page.go_forward()

    def accept_cookies(self):

        self.page.wait_for_load_state("domcontentloaded")

        cookie_popup = self.page.get_by_role(
            "dialog",
            name="Cookie consent"
        )

        if cookie_popup.is_visible():

            accept_button = cookie_popup.get_by_role(
                "button",
                name="Accept",
                exact=True
            )

            accept_button.click()

            print("Cookie consent accepted successfully!")

    # Close the promotional popup if it appears.
    def close_promo_popup(self):

        # Locate the close button inside the promotional popup.
        promo_close_button = self.page.locator(
            "form#WebPop button:has(span.icon-close-rounded)"
        )

        # Check whether the popup is currently visible.
        if promo_close_button.is_visible():

            # Click the close button.
            promo_close_button.click()

            print("Promotional popup closed successfully!")

        else:
            print("Promotional popup was not displayed!")

            # Close the promotional popup if it appears.
    
    # Close the promotional popup if it appears.
    def close_promo_popup(self):

        # Locate the actual close button inside the promotional form.
        promo_close_button = self.page.locator(
            "form#WebPop button:has(span.icon-close-rounded)"
        )

        try:
            # Wait until the promotional close button appears.
            promo_close_button.wait_for(
                state="visible",
                timeout=15000
            )

            # Click the close button.
            promo_close_button.click()

            # Verify that the close button disappears.
            promo_close_button.wait_for(
                state="hidden",
                timeout=5000
            )

            print("Promotional popup closed successfully!")

        except Exception as error:
            print(f"Could not close promotional popup: {error}")
            raise
