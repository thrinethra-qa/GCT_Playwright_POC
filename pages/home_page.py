
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

        # Close the promotional popup if it appears.
        # This prevents it from interfering with navigation.
        self.close_promo_popup()

        # Locate the Special Offers link directly.
        # We avoid restricting the search to a navigation
        # region named "Main".
        special_offer = self.page.get_by_role(
            "link",
            name="Special Offers",
            exact=True
        ).first

        # Wait until the navigation link becomes visible.
        special_offer.wait_for(
            state="visible",
            timeout=15000
        )

        # Click the Special Offers navigation link.
        special_offer.click()

        # Wait until the Special Offers page opens.
        self.page.wait_for_url(
            "**/special-offers**",
            timeout=15000
        )

        print("Special Offers navigation completed successfully!")
