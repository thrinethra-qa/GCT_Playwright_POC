
from pages.home_page import HomePage


def test_special_offers_page_navigation(browser_page):
    # Create the HomePage object using the existing browser fixture.
    home = HomePage(browser_page)

    # Open the GCT homepage.
    home.open_homepage()

    print("Homepage opened successfully!")

    # Click the Special Offers link.
    home.open_special_offers()

    # Verify that the Special Offers page URL is correct.
    assert "/special-offers" in browser_page.url, (
        "Special Offers page did not open successfully!"
    )

    # Verify that the page has loaded.
    browser_page.wait_for_load_state("domcontentloaded")

    print("TC13 - Special Offers page navigation verified!")

