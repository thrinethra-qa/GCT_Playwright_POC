from pages.home_page import HomePage


def test_browser_back_navigation(browser_page):
    home = HomePage(browser_page)

    # Open homepage
    home.open_homepage()
    print("Homepage opened successfully!")

    # Navigate to Special Offers
    home.open_special_offers()

    assert "/special-offers" in browser_page.url
    print("Special Offers page opened successfully!")

    # Perform browser Back navigation
    home.go_back()

    # Verify navigation to homepage
    assert browser_page.url.rstrip("/") == "https://www.gct.com"
    print("Browser Back navigation successful!")