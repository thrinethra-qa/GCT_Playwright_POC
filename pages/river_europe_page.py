
import re

from pages.base_page import BasePage
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError


class RiverEuropePage(BasePage):

    def __init__(self, page):
        # Initialize common browser methods from BasePage.
        super().__init__(page)

        # TC16: Locate the Rivers of Europe tab.
        self.rivers_of_europe_tab = self.page.locator(
            "xpath=//button[@id='radix-_R_4a5fivdb_-trigger-1']"
        )

        # TC17: Locate the Holland & Belgium cruise link.
        self.holland_belgium_link = self.page.get_by_role(
            "link",
            name="Holland & Belgium in Springtime",
            exact=True
        )

        # TC18: Locate the View dates and prices link.
        self.view_dates_prices_link = self.page.locator(
            "xpath=//a[normalize-space()='View dates and prices']"
        )

        # TC19: Locate the March departure options.
        self.march_options = self.page.get_by_role(
            "button",
            name=re.compile(r"March.*From", re.IGNORECASE)
        )

        # Locate all Select Date buttons.
        self.select_date_buttons = self.page.get_by_role(
            "button",
            name="Select Date"
        )

        # Locate Category C cabin.
        self.category_c_cabin = self.page.get_by_label(
            "Category C",
            exact=True
        )

        # TC20: Locate the Next: Trip Extensions button.
        self.next_trip_extensions_button = self.page.get_by_role(
            "button",
            name="Next: Trip Extensions"
        )

        # Locate the Bruges extension heading.
        self.bruges_extension = self.page.get_by_role(
            "heading",
            name="Bruges, Belgium",
            exact=True
        ).first

        # Locate the Add to Trip button.
        self.add_to_trip_button = self.page.get_by_role(
            "button",
            name="Add to Trip",
            exact=True
        ).first

        # Locate the Amsterdam unavailable message.
        self.amsterdam_unavailable_message = self.page.get_by_text(
            "Pre-Trip Extension not available on this departure date",
            exact=True
        )

        # Locate the Next: Pricing Summary button.
        self.next_pricing_summary_button = self.page.get_by_role(
            "button",
            name="Next: Pricing Summary"
        )

    # ---------------------------------------------------------
    # Common helper: dismiss a blocking overlay if displayed.
    # ---------------------------------------------------------

    def dismiss_blocking_overlay(self):

        # First try closing the known promotional popup.
        self.close_promo_popup()

        # Locate the full-screen Radix overlay.
        overlay = self.page.locator(
            "div.fixed.inset-0.z-50"
        ).first

        try:
            # Check whether the overlay is visible.
            overlay.wait_for(
                state="visible",
                timeout=1500
            )

            # Try dismissing the popup using Escape.
            self.page.keyboard.press("Escape")

            # Wait for the overlay to disappear.
            overlay.wait_for(
                state="hidden",
                timeout=5000
            )

            print("Blocking overlay dismissed successfully!")

        except PlaywrightTimeoutError:
            print("No dismissible blocking overlay was detected.")

    # ---------------------------------------------------------
    # TC16: Verify Rivers of Europe navigation.
    # ---------------------------------------------------------

    def click_rivers_of_europe_tab(self):

        # Dismiss any popup before clicking.
        self.dismiss_blocking_overlay()

        # Verify that the tab is visible.
        expect(self.rivers_of_europe_tab).to_be_visible(
            timeout=15000
        )

        # Click the Rivers of Europe tab.
        self.rivers_of_europe_tab.click(
            timeout=15000
        )

        print("Rivers of Europe tab clicked successfully!")

    # ---------------------------------------------------------
    # TC16: Verify river cruises are displayed.
    # ---------------------------------------------------------

    def verify_river_cruises_displayed(self):

        # Confirm that the Holland & Belgium cruise is visible.
        expect(self.holland_belgium_link).to_be_visible(
            timeout=15000
        )

        print("River cruises are displayed successfully!")

    # ---------------------------------------------------------
    # TC17: Select Holland & Belgium cruise.
    # TEMPORARY DIAGNOSTIC: Inspect the blocking popup.
    # ---------------------------------------------------------

    def click_holland_belgium_cruise(self):

        # Locate the Black Friday popup dialog.
        dialog = self.page.locator(
            '[role="dialog"][aria-describedby="web-popup-description"]'
        )

        # Print popup details if the dialog is displayed.
        if dialog.is_visible():

            print("\n========== POPUP TEXT ==========")
            print(dialog.inner_text())

            print("\n========== POPUP BUTTON DETAILS ==========")

            # Find all buttons inside the popup.
            buttons = dialog.locator("button")

            for index in range(buttons.count()):

                button = buttons.nth(index)

                # Print each button's text and HTML attributes.
                button_details = button.evaluate(
                    """element => ({
                        text: element.innerText,
                        ariaLabel: element.getAttribute('aria-label'),
                        title: element.getAttribute('title'),
                        html: element.outerHTML
                    })"""
                )

                print(f"Button {index}: {button_details}")

            print("========== END POPUP DETAILS ==========\n")

        # Wait until the Holland & Belgium link is visible.
        expect(self.holland_belgium_link).to_be_visible(
            timeout=15000
        )

        # Attempt the click so the diagnostic output is captured
        # even if the popup is still blocking the link.
        self.holland_belgium_link.click(
            timeout=15000
        )

        print("Holland & Belgium cruise clicked successfully!")

    # ---------------------------------------------------------
    # TC17: Verify Holland & Belgium cruise overview.
    # ---------------------------------------------------------

    def verify_holland_belgium_overview(self):

        # Verify the cruise title on the overview page.
        expect(
            self.page.locator("h1[data-epi-edit='TripTitle']")
        ).to_contain_text(
            "Holland & Belgium in Springtime",
            timeout=15000
        )

        print("Holland & Belgium cruise overview displayed!")

    # ---------------------------------------------------------
    # TC18: Navigate to View dates and prices.
    # ---------------------------------------------------------

    def click_view_dates_and_prices(self):

        # Dismiss any popup or blocking overlay.
        self.dismiss_blocking_overlay()

        # Verify that the link is visible.
        expect(self.view_dates_prices_link).to_be_visible(
            timeout=15000
        )

        # Click View dates and prices.
        self.view_dates_prices_link.click(
            timeout=15000
        )

        print("View dates and prices link clicked successfully!")

        # Check for any popup after navigation.
        self.dismiss_blocking_overlay()

    # ---------------------------------------------------------
    # TC18: Verify Departure Details page.
    # ---------------------------------------------------------

    def verify_departure_details_page(self):

        # Locate the Departure Details tab.
        departure_details_tab = self.page.get_by_role(
            "tab",
            name="1 Departure Details"
        )

        # Verify that the tab is visible.
        expect(departure_details_tab).to_be_visible(
            timeout=15000
        )

        # Verify that the tab is selected.
        expect(departure_details_tab).to_have_attribute(
            "aria-selected",
            "true"
        )

        print("Departure Details page opened successfully!")
        print("Departure Details tab is selected!")

    # ---------------------------------------------------------
    # TC19: Expand March 2027 departure dates.
    # ---------------------------------------------------------

    def expand_march_2027_dates(self):

        # Dismiss any popup or blocking overlay.
        self.dismiss_blocking_overlay()

        # Verify that the March option is visible.
        expect(self.march_options.first).to_be_visible(
            timeout=15000
        )

        # Expand the first March departure option.
        self.march_options.first.click(
            timeout=15000
        )

        print("March 2027 departure dates expanded!")

    # ---------------------------------------------------------
    # TC19: Select March 26, 2027 departure.
    # ---------------------------------------------------------

    def select_march_26_departure(self):

        # Dismiss any popup or blocking overlay.
        self.dismiss_blocking_overlay()

        # Wait for the second Select Date button.
        expect(self.select_date_buttons.nth(1)).to_be_visible(
            timeout=15000
        )

        # Select the March 26 departure date.
        self.select_date_buttons.nth(1).click(
            timeout=15000
        )

        print("March 26 - April 6, 2027 departure selected!")

    # ---------------------------------------------------------
    # TC19: Verify cabin options.
    # ---------------------------------------------------------

    def verify_cabin_options_displayed(self):

        # Confirm that Category C cabin is visible.
        expect(self.category_c_cabin).to_be_visible(
            timeout=15000
        )

        # Confirm that the Category C text is displayed.
        expect(
            self.category_c_cabin.get_by_text(
                "Category C",
                exact=True
            )
        ).to_be_visible()

        print("Cabin options are displayed successfully!")

    # ---------------------------------------------------------
    # TC19: Select Category C cabin.
    # ---------------------------------------------------------

    def select_category_c_cabin(self):

        # Dismiss any popup or blocking overlay.
        self.dismiss_blocking_overlay()

        # Locate the Select Cabins option inside Category C.
        select_cabin = self.category_c_cabin.get_by_text(
            "Select Cabins",
            exact=True
        )

        # Verify that the option is visible.
        expect(select_cabin).to_be_visible(
            timeout=15000
        )

        # Select Category C.
        select_cabin.click(
            timeout=15000
        )

        # Verify that the cabin is selected.
        expect(
            self.category_c_cabin.get_by_text(
                "Selected",
                exact=True
            )
        ).to_be_visible(
            timeout=15000
        )

        print("Category C cabin selected successfully!")

    # ---------------------------------------------------------
    # TC20: Navigate to Trip Extensions.
    # ---------------------------------------------------------

    def click_next_trip_extensions(self):

        # Dismiss any popup or blocking overlay.
        self.dismiss_blocking_overlay()

        # Verify that the Next button is visible.
        expect(self.next_trip_extensions_button).to_be_visible(
            timeout=15000
        )

        # Click Next: Trip Extensions.
        self.next_trip_extensions_button.click(
            timeout=15000
        )

        print("Next: Trip Extensions clicked successfully!")

    # ---------------------------------------------------------
    # TC20: Verify Trip Extensions page.
    # ---------------------------------------------------------

    def verify_trip_extensions_page(self):

        # Dismiss any popup or blocking overlay.
        self.dismiss_blocking_overlay()

        # Verify that the Bruges extension is displayed.
        expect(self.bruges_extension).to_be_visible(
            timeout=15000
        )

        # Verify that the Add to Trip button is displayed.
        expect(self.add_to_trip_button).to_be_visible(
            timeout=15000
        )

        # Verify that Amsterdam is unavailable.
        expect(
            self.amsterdam_unavailable_message
        ).to_be_visible(
            timeout=15000
        )

        print("Trip Extensions page displayed successfully!")
        print("Bruges extension is available!")
        print("Amsterdam pre-trip extension availability verified!")

    # ---------------------------------------------------------
    # TC20: Navigate to Pricing Summary.
    # ---------------------------------------------------------

    def click_next_pricing_summary(self):

        # Dismiss any popup or blocking overlay.
        self.dismiss_blocking_overlay()

        # Verify that the Next button is visible.
        expect(self.next_pricing_summary_button).to_be_visible(
            timeout=15000
        )

        # Click Next: Pricing Summary.
        self.next_pricing_summary_button.click(
            timeout=15000
        )

        print("Next: Pricing Summary clicked successfully!")

    # ---------------------------------------------------------
    # TC20: Verify Pricing Summary page.
    # ---------------------------------------------------------

    def verify_pricing_summary_page(self):

        # Dismiss any popup or blocking overlay.
        self.dismiss_blocking_overlay()

        # Locate the Pricing Summary tab.
        pricing_summary_tab = self.page.get_by_role(
            "tab",
            name=re.compile(
                r"4 Pricing Summary",
                re.IGNORECASE
            )
        )

        # Verify that Pricing Summary is visible.
        expect(pricing_summary_tab).to_be_visible(
            timeout=15000
        )

        # Verify that Pricing Summary is selected.
        expect(pricing_summary_tab).to_have_attribute(
            "aria-selected",
            "true"
        )

        print("Pricing Summary page opened successfully!")
        print("Pricing Summary tab is selected!")
