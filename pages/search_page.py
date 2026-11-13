
import re

from pages.base_page import BasePage
from playwright.sync_api import expect


class SearchPage(BasePage):

    def __init__(self, page):
        # Initialize common methods from BasePage.
        super().__init__(page)

        # Locate the destination search field.
        self.search_field = self.page.locator(
            "//input[@id='_R_5cn5b_']"
        )

        # Locate the visible Europe autocomplete suggestion.
        # The URL may contain additional query parameters.
        self.europe_suggestion = (
            self.page.locator(
                "a[href*='/tripsavailable']:visible"
            )
            .filter(
                has_text=re.compile(
                    r"Europe",
                    re.IGNORECASE
                )
            )
            .first
        )

        # Locate the no-results message.
        self.no_results_message = self.page.get_by_text(
            re.compile(
                r"No results found",
                re.IGNORECASE
            )
        )

    # ---------------------------------------------------------
    # COMMON SEARCH PREPARATION
    # ---------------------------------------------------------

    def prepare_search(self):

        # Accept the cookie popup if it appears.
        self.accept_cookies()

        # Close the promotional popup if it appears.
        self.close_promo_popup()

        # Verify that the destination search field is available.
        expect(
            self.search_field
        ).to_be_visible(timeout=15000)

        expect(
            self.search_field
        ).to_be_enabled(timeout=15000)

    # ---------------------------------------------------------
    # VERIFY DESTINATION SEARCH FIELD
    # ---------------------------------------------------------

    def is_search_visible(self):

        # Return True if the search field is visible.
        return self.search_field.is_visible()

    def is_search_enabled(self):

        # Return True if the search field is enabled.
        return self.search_field.is_enabled()

    # ---------------------------------------------------------
    # TC07 - VALID DESTINATION SEARCH
    # ---------------------------------------------------------

    def get_visible_europe_suggestion(self):

        # Return the visible Europe suggestion.
        return self.europe_suggestion

    def search_valid_destination(self, destination):

        # Step 1: Prepare the homepage for searching.
        self.prepare_search()

        # Step 2: Enter the valid destination.
        self.search_field.fill(destination)

        # Step 3: Wait for the Europe suggestion.
        expect(
            self.europe_suggestion
        ).to_be_visible(timeout=20000)

        # Step 4: Close the promotional popup if it appears.
        self.close_promo_popup()

        # Step 5: Verify that Europe is still visible.
        expect(
            self.europe_suggestion
        ).to_be_visible(timeout=15000)

        # Step 6: Click the Europe suggestion.
        self.europe_suggestion.click(timeout=15000)

        # Step 7: Wait for navigation to begin.
        # "commit" avoids waiting for advertisements and other
        # resources that may delay the complete page load.
        self.page.wait_for_url(
            "**/tripsavailable*",
            wait_until="commit",
            timeout=30000
        )

        # Step 8: Verify that the URL contains Europe.
        expect(
            self.page
        ).to_have_url(
            re.compile(
                r"tripsavailable.*Europe",
                re.IGNORECASE
            ),
            timeout=15000
        )

        print("Valid destination URL:", self.page.url)
        print("Europe destination search completed successfully!")

    # ---------------------------------------------------------
    # TC08 - INVALID DESTINATION SEARCH
    # ---------------------------------------------------------

    def search_invalid_destination(self, destination):

        # Step 1: Prepare the homepage for searching.
        self.prepare_search()

        # Step 2: Enter the invalid destination.
        self.search_field.fill(destination)

        # Step 3: Close the promotional popup if it appears.
        self.close_promo_popup()

        # Step 4: Submit the invalid destination.
        self.search_field.press("Enter")

        # Step 5: Wait for the no-results message.
        # Do not assume that the website must navigate to a
        # particular URL for an invalid destination.
        expect(
            self.no_results_message
        ).to_be_visible(timeout=15000)

        print("Invalid destination search completed!")
        print("No-results message displayed successfully!")

    def is_no_results_message_displayed(self):

        # Check whether the no-results message is visible.
        return self.no_results_message.is_visible()

    # ---------------------------------------------------------
    # TC09 - PARTIAL DESTINATION SUGGESTIONS
    # ---------------------------------------------------------

    def search_partial_destination(self, destination):

        # Step 1: Prepare the homepage for searching.
        self.prepare_search()

        # Step 2: Enter the partial destination.
        self.search_field.fill(destination)

        print("Partial destination entered:", destination)

    def is_europe_suggestion_displayed(self):

        # Step 3: Verify that Europe appears in suggestions.
        expect(
            self.europe_suggestion
        ).to_be_visible(timeout=15000)

        return self.europe_suggestion.is_visible()
