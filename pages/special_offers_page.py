
from pages.base_page import BasePage
from playwright.sync_api import expect
import re


class SpecialOffersPage(BasePage):

    def __init__(self, page):
        # Initialize common browser methods from BasePage.
        super().__init__(page)

        # Locator for the main content area of the Special Offers page.
        self.main_content = self.page.locator("main")

        # --------------------------------------------------
        # TC14: Original and discounted price locators
        # --------------------------------------------------

        # Locator for the original price in the first offer row.
        self.original_price = self.page.locator(
            "xpath=//body[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[3]"
        )

        # Locator for the discounted price in the first offer row.
        self.discounted_price = self.page.locator(
            "xpath=//body[1]/main[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[4]"
        )

        # --------------------------------------------------
        # TC15: Offer details navigation locators
        # --------------------------------------------------

        # Locator for the first View Trip Details link.
        self.offer_details_link = self.page.locator(
            "xpath=//a[normalize-space()='View Trip Details']"
        ).first

        # Locator for the expected trip details page heading.
        self.trip_details_heading = self.page.locator(
            "xpath=//h1[normalize-space()='The Seine: Paris & the Heart of Normandy']"
        )

    # ==================================================
    # TC13: Verify Special Offers page
    # ==================================================

    def verify_special_offers_page(self):

        # Verify that the current URL contains special-offers.
        expect(self.page).to_have_url(
            re.compile(r".*/special-offers.*"),
            timeout=15000
        )

        # Verify that the main content is visible.
        expect(self.main_content).to_be_visible()

        # Get the text displayed inside the main content.
        page_content = self.main_content.inner_text()

        # Check that the page is not empty.
        assert page_content.strip(), (
            "Special Offers page content is empty!"
        )

        print("Special Offers page loaded successfully!")
        print("Special Offers page content is displayed!")

    # ==================================================
    # TC14: Verify original and discounted prices
    # ==================================================

    def verify_original_and_discounted_prices(self):

        # Verify that the original price is visible.
        expect(self.original_price).to_be_visible(
            timeout=10000
        )

        # Verify that the discounted price is visible.
        expect(self.discounted_price).to_be_visible(
            timeout=10000
        )

        # Read the original price from the page.
        original = self.original_price.inner_text()

        # Read the discounted price from the page.
        discounted = self.discounted_price.inner_text()

        # Print both prices in the terminal.
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

        # Wait until the first offer details link is visible.
        expect(self.offer_details_link).to_be_visible(
            timeout=10000
        )

        # Click the first View Trip Details link.
        self.offer_details_link.click()

        print("First offer details link clicked successfully!")

    def verify_offer_trip_details_page(self):

        # Verify that the expected trip heading is visible.
        expect(self.trip_details_heading).to_be_visible(
            timeout=15000
        )

        # Get the heading text from the trip details page.
        heading = self.trip_details_heading.inner_text()

        # Print the heading as test execution evidence.
        print(f"Trip details heading displayed: {heading}")

        print(
            "TC15 - Offer trip details page opened successfully!"
        )
