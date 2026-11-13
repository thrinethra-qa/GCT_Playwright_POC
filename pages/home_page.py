
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, page):
        # Initialize common browser methods from BasePage.
        super().__init__(page)

    def open_homepage(self):
        # Navigate to the GCT homepage.
        self.navigate("https://www.gct.com/")

    def click_logo(self):
        # Locate the visible GCT logo and click it.
        self.page.locator(
            ".global-header-logo a:visible"
        ).click()

        # Verify that the browser returns to the homepage.
        self.page.wait_for_url("https://www.gct.com/")

    def open_special_offers(self):

        # First, handle a promotional popup if it is already visible.
        self.close_promo_popup()

        # Locate the Special Offers navigation link.
        special_offer = self.page.get_by_role(
            "link",
            name="Special Offers",
            exact=True
        ).first

        # Wait for the navigation link.
        special_offer.wait_for(
            state="visible",
            timeout=15000
        )

        # Try the normal click first.
        try:
            special_offer.click(timeout=5000)

        except PlaywrightTimeoutError:

            # If the click is blocked, check for a delayed popup.
            print(
                "Navigation click was blocked. "
                "Checking for a promotional popup..."
            )

            popup_closed = self.close_promo_popup(
                wait_timeout=3000
            )

            if not popup_closed:
                # If no popup was found, allow Playwright to retry.
                print(
                    "No promotional popup found. "
                    "Retrying the navigation click."
                )

            # Retry the navigation after popup handling.
            special_offer.click(timeout=10000)

        # Wait until the Special Offers page opens.
        self.page.wait_for_url(
            "**/special-offers**",
            timeout=15000
        )

        print("Special Offers navigation completed successfully!")
