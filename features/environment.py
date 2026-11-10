
import os
from pathlib import Path
import allure

from playwright.sync_api import sync_playwright


def before_all(context):
    # Start Playwright before executing the feature files.
    context.playwright = sync_playwright().start()

    # GitHub Actions automatically sets CI=true.
    # Locally, the browser remains visible.
    # In CI/CD, the browser runs in headless mode.
    is_ci = os.getenv("CI", "false").lower() == "true"

    context.browser = context.playwright.chromium.launch(
        headless=is_ci
    )

    print(f"\nPlaywright browser launched successfully! Headless mode: {is_ci}")


def before_scenario(context, scenario):

    # Create folders to store screenshots and videos.
    screenshot_dir = Path("screenshots")
    video_dir = Path("videos")

    screenshot_dir.mkdir(parents=True, exist_ok=True)
    video_dir.mkdir(parents=True, exist_ok=True)

    # Create a safe filename using the scenario name.
    safe_name = scenario.name.replace(" ", "_")

    # Create a separate video folder for each scenario.
    scenario_video_dir = video_dir / safe_name
    scenario_video_dir.mkdir(parents=True, exist_ok=True)

    # Create a new browser context for the scenario.
    # Video recording is enabled for every scenario.
    context.browser_context = context.browser.new_context(
        record_video_dir=str(scenario_video_dir),
        record_video_size={
            "width": 1280,
            "height": 720
        }
    )

    # Open a new browser page.
    context.page = context.browser_context.new_page()

    # Store the scenario name and screenshot path.
    context.scenario_name = safe_name
    context.screenshot_path = screenshot_dir / f"{safe_name}.png"

    print(f"\nStarting scenario: {scenario.name}")


def after_scenario(context, scenario):

    # Capture a screenshot before closing the browser context.
    context.page.screenshot(
        path=str(context.screenshot_path),
        full_page=True
    )

    # Attach the screenshot to the Allure report.
    allure.attach.file(
        str(context.screenshot_path),
        name=f"{scenario.name} - Screenshot",
        attachment_type=allure.attachment_type.PNG
    )

    # Print the screenshot path when a scenario fails.
    if scenario.status == "failed" or scenario.status == "error":
        print(f"Failure screenshot saved: {context.screenshot_path}")

    # Save the video object before closing the browser context.
    video = context.page.video

    # Close the context to finalize the video recording.
    context.browser_context.close()

    # Attach the finalized video to the Allure report.
    if video is not None:
        video_path = video.path()

        allure.attach.file(
            str(video_path),
            name=f"{scenario.name} - Video",
            attachment_type="video/webm",
            extension="webm"
        )

        print(f"Video saved: {video_path}")

    print(f"Scenario status: {scenario.status}")


def after_all(context):

    # Close the browser after all scenarios finish.
    context.browser.close()

    # Stop Playwright.
    context.playwright.stop()

    print("\nPlaywright browser closed successfully!")
