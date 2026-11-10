from pages.home_page import HomePage


def test_logo_navigation(browser_page):
    home = HomePage(browser_page)

    # Open homepage
    home.open_homepage()
    print("Homepage opened successfully!")

    # Click Special Offers
    home.open_special_offers()

    assert "/special-offers" in browser_page.url
    print("Special Offers link clicked successfully!")

    # Click GCT logo
    home.click_logo()

    # Verify homepage navigation
    assert browser_page.url.rstrip("/") == "https://www.gct.com"
    print("GCT logo clicked successfully! Returned to homepage.")