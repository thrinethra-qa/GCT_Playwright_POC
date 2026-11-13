
from pages.base_page import BasePage
from playwright.sync_api import expect
import re


class SpecialOffersPage(BasePage):

    def __init__(self, page):
        # Initialize common browser methods from BasePage.
        super().__init__(page)

        # Locator for the main content area.
        self.main_content = self.page.locator("main")

        # --------------------------------------------------
        # TC14: Original and discounted price locators
        # --------------------------------------------------

        self.original_price = self.page.locator(
            "xpath=//body[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[3]"
        )

        self.discounted_price = self.page.locator(
            "xpath=//body[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[4]"
        )

        # --------------------------------------------------
        # TC15: Offer details navigation locator
        # --------------------------------------------------

        self.offer_details_link = self.page.locator(
            "xpath=//a[normalize-space()='View Trip Details']"
        ).first

    # ==================================================
    # TC13: Verify Special Offers page
    # ==================================================

    def verify_special_offers_page(self):

        expect(self.page).to_have_url(
            re.compile(r".*/special-offers.*"),
            timeout=15000
        )

        expect(self.main_content).to_be_visible()

        page_content = self.main_content.inner_text()

        assert page_content.strip(), (
            "Special Offers page content is empty!"
        )

        print("Special Offers page loaded successfully!")
        print("Special Offers page content is displayed!")

    # ==================================================
    # TC14: Verify original and discounted prices
    # ==================================================

    def verify_original_and_discounted_prices(self):

        expect(self.original_price).to_be_visible(
            timeout=10000
        )

        expect(self.discounted_price).to_be_visible(
            timeout=10000
        )

        original = self.original_price.inner_text()
        discounted = self.discounted_price.inner_text()

        print(f"Original price displayed: {original}")
        print(f"Discounted price displayed: {discounted}")

        print(
            "TC14 - Original and discounted prices "
            "are displayed successfully!"
        )

    # ==================================================
    # TC15: Verify offer details navigation
    # ==================================================

    def click_first_offer_details(self):

        # Close the promotional popup BEFORE clicking.
        # This prevents the popup from intercepting the link.
        self.close_promo_popup()

        # Wait until the first offer details link is visible.
        expect(self.offer_details_link).to_be_visible(
            timeout=15000
        )

        # Ensure the link is enabled before clicking.
        expect(self.offer_details_link).to_be_enabled(
            timeout=10000
        )

        # Click the first View Trip Details link.
        self.offer_details_link.click(timeout=15000)

        # Wait until the destination page starts loading.
        self.page.wait_for_load_state(
            "domcontentloaded",
            timeout=15000
        )

        print("First offer details link clicked successfully!")

    def verify_offer_trip_details_page(self):

        actual_heading = self.page.locator("main h1").first

        expect(actual_heading).to_be_visible(
            timeout=15000
        )

        heading = actual_heading.inner_text().strip()

        assert heading, "Trip details page heading is empty!"

        print(f"Trip details heading displayed: {heading}")

        print(
            "TC15 - Offer trip details page opened successfully!"
        )
