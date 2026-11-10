
import re

from pages.base_page import BasePage
from playwright.sync_api import expect


class RiverEuropePage(BasePage):

    def __init__(self, page):
        # Initialize common browser methods from BasePage.
        super().__init__(page)

        # TC16: Locate the Rivers of Europe tab.
        self.rivers_of_europe_tab = self.page.locator(
            "xpath=//button[@id='radix-_R_4a5fivdb_-trigger-1']"
        )

        # TC17: Locate the Holland and Belgium cruise link.
        self.holland_belgium_link = self.page.get_by_role(
            "link",
            name="Holland & Belgium in Springtime",
            exact=True
        )

        # TC18: Locate the View dates and prices link.
        self.view_dates_prices_link = self.page.locator(
            "xpath=//a[normalize-space()='View dates and prices']"
        )

        # TC19: Locate the March departure accordion.
        # Regex allows the button name to contain additional price information.
        self.march_options = self.page.get_by_role(
            "button",
            name=re.compile(r"March.*From", re.IGNORECASE)
        )

        # Locate all Select Date buttons.
        self.select_date_buttons = self.page.get_by_role(
            "button",
            name="Select Date"
        )

        # Locate the Category C cabin option.
        self.category_c_cabin = self.page.get_by_label(
            "Category C",
            exact=True
        )

        # Locate the button to continue to Trip Extensions.
        self.next_trip_extensions_button = self.page.get_by_role(
            "button",
            name="Next: Trip Extensions"
        )

        # TC20: Two extension cards contain the same Bruges heading.
        # Use the first heading to avoid Playwright strict-mode errors.
        self.bruges_extension = self.page.get_by_role(
            "heading",
            name="Bruges, Belgium",
            exact=True
        ).first

        # Two extension cards contain an Add to Trip button.
        # Use the first button to verify the Pre-Trip Extension card.
        self.add_to_trip_button = self.page.get_by_role(
            "button",
            name="Add to Trip",
            exact=True
        ).first

        # Locate the message indicating Amsterdam is unavailable.
        self.amsterdam_unavailable_message = self.page.get_by_text(
            "Pre-Trip Extension not available on this departure date",
            exact=True
        )

        # Locate the button to continue to Pricing Summary.
        self.next_pricing_summary_button = self.page.get_by_role(
            "button",
            name="Next: Pricing Summary"
        )

    # ---------------------------------------------------------
    # TC16: Verify Rivers of Europe navigation
    # ---------------------------------------------------------

    def click_rivers_of_europe_tab(self):
        # Check that the tab is visible before clicking.
        expect(self.rivers_of_europe_tab).to_be_visible(timeout=15000)

        self.rivers_of_europe_tab.click()

        print("Rivers of Europe tab clicked successfully!")

    def verify_river_cruises_displayed(self):
        # Verify that the expected river cruise link is displayed.
        expect(self.holland_belgium_link).to_be_visible(timeout=15000)

        print("River cruises are displayed successfully!")

    # ---------------------------------------------------------
    # TC17: Verify Holland and Belgium cruise selection
    # ---------------------------------------------------------

    def click_holland_belgium_cruise(self):
        # Check that the cruise link is visible before clicking.
        expect(self.holland_belgium_link).to_be_visible(timeout=15000)

        self.holland_belgium_link.click()

        print("Holland & Belgium cruise selected successfully!")

    def verify_holland_belgium_overview(self):
        # Verify that the cruise overview displays the expected title.
        expect(
            self.page.locator("h1[data-epi-edit='TripTitle']")
        ).to_contain_text(
            "Holland & Belgium in Springtime",
            timeout=15000
        )

        print("Holland & Belgium cruise overview displayed!")

    # ---------------------------------------------------------
    # TC18: Verify View dates and prices navigation
    # ---------------------------------------------------------

    def click_view_dates_and_prices(self):
        # Wait until the View dates and prices link is visible.
        expect(self.view_dates_prices_link).to_be_visible(timeout=15000)

        self.view_dates_prices_link.click()

        print("View dates and prices link clicked successfully!")

        # Close the promotional popup if it appears.
        self.close_promo_popup()

    def verify_departure_details_page(self):
        # Locate the Departure Details tab.
        departure_details_tab = self.page.get_by_role(
            "tab",
            name="1 Departure Details"
        )

        # Verify that the tab is visible and selected.
        expect(departure_details_tab).to_be_visible(timeout=15000)

        expect(departure_details_tab).to_have_attribute(
            "aria-selected",
            "true"
        )

        print("Departure Details page opened successfully!")
        print("Departure Details tab is selected!")

    # ---------------------------------------------------------
    # TC19: Verify departure date and cabin selection
    # ---------------------------------------------------------

    def expand_march_2027_dates(self):
        # Select the first March accordion (March 2027).
        expect(self.march_options.first).to_be_visible(timeout=15000)

        self.march_options.first.click()

        print("March 2027 departure dates expanded!")

    def select_march_26_departure(self):
        # Select the second Select Date button.
        # This corresponds to the March 26 departure in the current page.
        expect(self.select_date_buttons.nth(1)).to_be_visible(timeout=15000)

        self.select_date_buttons.nth(1).click()

        print("March 26 - April 6, 2027 departure selected!")

    def verify_cabin_options_displayed(self):
        # Verify that Category C cabin information is displayed.
        expect(self.category_c_cabin).to_be_visible(timeout=15000)

        expect(
            self.category_c_cabin.get_by_text(
                "Category C",
                exact=True
            )
        ).to_be_visible()

        print("Cabin options are displayed successfully!")

    def select_category_c_cabin(self):
        # Locate the Select Cabins option inside Category C.
        select_cabin = self.category_c_cabin.get_by_text(
            "Select Cabins",
            exact=True
        )

        expect(select_cabin).to_be_visible(timeout=15000)

        # Select Category C.
        select_cabin.click()

        # Verify that the cabin selection was successful.
        expect(
            self.category_c_cabin.get_by_text(
                "Selected",
                exact=True
            )
        ).to_be_visible(timeout=15000)

        print("Category C cabin selected successfully!")

    def click_next_trip_extensions(self):
        # Click the button to move to the Trip Extensions stage.
        expect(
            self.next_trip_extensions_button
        ).to_be_visible(timeout=15000)

        self.next_trip_extensions_button.click()

        print("Next: Trip Extensions clicked successfully!")

    # ---------------------------------------------------------
    # TC20: Verify Trip Extensions and Pricing Summary
    # ---------------------------------------------------------

    def verify_trip_extensions_page(self):
        # Verify that the Bruges extension heading is displayed.
        expect(self.bruges_extension).to_be_visible(timeout=15000)

        # Verify that the first Add to Trip button is displayed.
        expect(self.add_to_trip_button).to_be_visible(timeout=15000)

        # Verify the Amsterdam pre-trip extension availability message.
        expect(
            self.amsterdam_unavailable_message
        ).to_be_visible(timeout=15000)

        print("Trip Extensions page displayed successfully!")
        print("Bruges extension is available!")
        print("Amsterdam pre-trip extension availability verified!")

    def click_next_pricing_summary(self):
        # Click the button to move to Pricing Summary.
        expect(
            self.next_pricing_summary_button
        ).to_be_visible(timeout=15000)

        self.next_pricing_summary_button.click()

        print("Next: Pricing Summary clicked successfully!")

    def verify_pricing_summary_page(self):
        # Locate the Pricing Summary tab.
        pricing_summary_tab = self.page.get_by_role(
            "tab",
            name=re.compile(r"4 Pricing Summary", re.IGNORECASE)
        )

        # Verify that Pricing Summary is visible and selected.
        expect(pricing_summary_tab).to_be_visible(timeout=15000)

        expect(pricing_summary_tab).to_have_attribute(
            "aria-selected",
            "true"
        )

        print("Pricing Summary page opened successfully!")
