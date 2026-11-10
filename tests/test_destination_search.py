from pages.search_page import SearchPage


def test_destination_search_field(browser_page):

    search = SearchPage(browser_page)

    browser_page.goto("https://www.gct.com/")

    assert search.is_search_visible(), "Search field is not visible"
    assert search.is_search_enabled(), "Search field is not enabled"