
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

    def search_valid_destination(self, destination):

        # Accept the cookie popup if it appears.
        self.accept_cookies()

        # Locate the destination search field.
        search_field = self.page.locator(
            "//input[@id='_R_5cn5b_']"
        )

        # Enter the valid destination.
        search_field.fill(destination)

        # Wait for autocomplete suggestions to appear.
        self.page.wait_for_timeout(2000)

        # Close the promotional popup if it appears.
        # This prevents the popup from blocking the suggestion click.
        self.close_promo_popup()

        # Locate the Europe region suggestion.
        suggestion = self.page.locator(
            "div.scroll-container"
        ).locator(
            'a[href="/tripsavailable?b=GN&r=Europe"]'
        ).first

        # Wait until the Europe suggestion is visible.
        suggestion.wait_for(
            state="visible",
            timeout=15000
        )

        # Click the matching suggestion.
        suggestion.click()

        # Wait until the Europe results page opens.
        self.page.wait_for_url(
            "**/tripsavailable?b=GN&r=Europe",
            timeout=15000
        )

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

        # Wait for the autocomplete suggestions to update.
        self.page.wait_for_timeout(1500)

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

        # Wait for the autocomplete suggestions to appear.
        self.page.wait_for_timeout(1500)

    def is_europe_suggestion_displayed(self):

        # Locate Europe under the Region suggestions.
        europe_suggestion = self.page.locator(
            "div.scroll-container"
        ).locator(
            'a[href="/tripsavailable?b=GN&r=Europe"]'
        ).first

        # Wait until the Europe suggestion becomes visible.
        europe_suggestion.wait_for(
            state="visible",
            timeout=10000
        )

        # Return whether the suggestion is visible.
        return europe_suggestion.is_visible()
