
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright


@pytest.fixture
def browser_page(request):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            yield page

        finally:
            # Check whether the test execution failed
            report = getattr(request.node, "rep_call", None)

            if report is not None and report.failed:
                screenshot_dir = Path("screenshots")
                screenshot_dir.mkdir(parents=True, exist_ok=True)

                screenshot_path = (
                    screenshot_dir / f"{request.node.name}.png"
                )

                page.screenshot(
                    path=str(screenshot_path),
                    full_page=True
                )

                print(f"Failure screenshot saved: {screenshot_path}")

            context.close()
            browser.close()


# Pytest hook to capture test execution reports
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    setattr(item, "rep_" + report.when, report)
