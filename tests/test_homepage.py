from pages.home_page import HomePage
#To open the url call the method from conftest and home_page.
def test_open_homepage(browser_page):
    home = HomePage(browser_page)

    home.open_homepage()

    assert "gct.com" in browser_page.url