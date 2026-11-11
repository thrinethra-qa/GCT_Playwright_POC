
from pages.base_page import BasePage


class SearchPage(BasePage):

    def __init__(self, page):
        # Initialize the parent BasePage and store the Playwright page.
        super().__init__(page)

    def is_search_visible(self):
        # Check whether the destination search field is visible.
        return self.page.locator(
            "//input[@id='_R_5cn5b_']"
        ).is_visible()

    def is_search_enabled(self):
        # Check whether the user can type into the search field.
        return self.page.locator(
            "//input[@id='_R_5cn5b_']"
        ).is_enabled()

    def get_visible_europe_suggestion(self):
        # Find only a visible Europe autocomplete link.
        # The :visible selector avoids matching hidden duplicate links.
        return self.page.locator(
            'a[href="/tripsavailable?b=GN&r=Europe"]:visible'
        ).first

    def search_valid_destination(self, destination):

        # Accept the cookie popup if it appears.
        self.accept_cookies()

        # Locate the destination search field.
        search_field = self.page.locator(
            "//input[@id='_R_5cn5b_']"
        )

        # Enter the valid destination.
        search_field.fill(destination)

        # Close the promotional popup if it appears.
        # This prevents the popup from blocking autocomplete interaction.
        self.close_promo_popup()

        # Locate the visible Europe suggestion.
        suggestion = self.get_visible_europe_suggestion()

        # Wait until the visible suggestion appears.
        suggestion.wait_for(
            state="visible",
            timeout=15000
        )

        # Click the visible Europe suggestion.
        suggestion.click()

        # Wait until the Europe results page opens.
        self.page.wait_for_url(
            "**/tripsavailable?b=GN&r=Europe",
            timeout=15000
        )

        # Print the resulting URL for debugging.
        print("Valid destination URL:", self.page.url)

    def search_invalid_destination(self, destination):

        # Accept the cookie popup if it appears.
        self.accept_cookies()

        # Locate the destination search field.
        search_field = self.page.locator(
            "//input[@id='_R_5cn5b_']"
        )

        # Enter the invalid destination.
        search_field.fill(destination)

        # Close the promotional popup if it appears.
        self.close_promo_popup()

        # Press Enter to submit the invalid search.
        search_field.press("Enter")

        # Wait for the search results URL.
        self.page.wait_for_url(
            "**/tripsavailable?b=GN&q=XYZ12345",
            timeout=15000
        )

        # Print the URL to help debug the test.
        print("Invalid destination URL:", self.page.url)

    def is_no_results_message_displayed(self):

        # Look for the no-results message.
        message = self.page.get_by_text(
            "No results found. Please try another keyword."
        )

        # Wait until the message becomes visible.
        message.wait_for(
            state="visible",
            timeout=10000
        )

        # Return True if the message is visible.
        return message.is_visible()

    def search_partial_destination(self, destination):

        # Accept cookies if the popup appears.
        self.accept_cookies()

        # Locate the destination search field.
        search_field = self.page.locator(
            "//input[@id='_R_5cn5b_']"
        )

        # Enter the partial destination.
        search_field.fill(destination)

    def is_europe_suggestion_displayed(self):

        # Locate only the visible Europe suggestion.
        europe_suggestion = self.get_visible_europe_suggestion()

        # Wait until the suggestion becomes visible.
        europe_suggestion.wait_for(
            state="visible",
            timeout=10000
        )

        # Return whether the suggestion is visible.
        return europe_suggestion.is_visible()
