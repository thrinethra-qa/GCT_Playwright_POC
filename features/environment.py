
import os
import re
from pathlib import Path
import allure

from playwright.sync_api import sync_playwright


def before_all(context):
    # Start Playwright before executing the feature files.
    context.playwright = sync_playwright().start()

    # Keep the browser visible locally and headless in CI/CD.
    is_ci = os.getenv("CI", "false").lower() == "true"

    context.browser = context.playwright.chromium.launch(
        headless=is_ci
    )

    print(
        f"\nPlaywright browser launched successfully! "
        f"Headless mode: {is_ci}"
    )


def before_scenario(context, scenario):

    # Create folders for screenshots, videos and traces.
    screenshot_dir = Path("screenshots")
    video_dir = Path("videos")
    trace_dir = Path("traces")

    screenshot_dir.mkdir(parents=True, exist_ok=True)
    video_dir.mkdir(parents=True, exist_ok=True)
    trace_dir.mkdir(parents=True, exist_ok=True)

    # Remove characters that Windows does not allow in filenames.
    safe_name = re.sub(
        r'[<>:"/\\|?*\x00-\x1f]',
        "_",
        scenario.name
    ).strip(" .")

    # Create a separate video folder for each scenario.
    scenario_video_dir = video_dir / safe_name
    scenario_video_dir.mkdir(parents=True, exist_ok=True)

    # Create a new browser context with video recording enabled.
    context.browser_context = context.browser.new_context(
        record_video_dir=str(scenario_video_dir),
        record_video_size={
            "width": 1280,
            "height": 720
        }
    )

    # Start tracing to capture browser actions and DOM snapshots.
    context.browser_context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    # Open a new browser page.
    context.page = context.browser_context.new_page()

    # Store output paths for the current scenario.
    context.scenario_name = safe_name
    context.screenshot_path = (
        screenshot_dir / f"{safe_name}.png"
    )
    context.trace_path = (
        trace_dir / f"{safe_name}_trace.zip"
    )

    print(f"\nStarting scenario: {scenario.name}")


def after_scenario(context, scenario):

    # Identify failed or errored scenarios.
    is_failed = scenario.status.name.lower() in (
        "failed",
        "error"
    )

    video = None
    trace_stopped = False

    try:
        # Save the video object before closing the page.
        video = context.page.video

        if is_failed:

            # Capture a screenshot only when the test fails.
            try:
                context.page.screenshot(
                    path=str(context.screenshot_path),
                    full_page=True
                )

                print(
                    f"Failure screenshot saved: "
                    f"{context.screenshot_path}"
                )

                # Attach the screenshot to the Allure report.
                allure.attach.file(
                    str(context.screenshot_path),
                    name=f"{scenario.name} - Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

            except Exception as error:
                print(
                    f"Screenshot capture failed: {error}"
                )

            # Save the Playwright trace for failed scenarios.
            try:
                context.browser_context.tracing.stop(
                    path=str(context.trace_path)
                )
                trace_stopped = True

                print(
                    f"Failure trace saved: {context.trace_path}"
                )

                # Attach the trace ZIP to Allure.
                allure.attach.file(
                    str(context.trace_path),
                    name=f"{scenario.name} - Playwright Trace",
                    attachment_type="application/zip",
                    extension="zip"
                )

            except Exception as error:
                print(
                    f"Trace saving failed: {error}"
                )

        else:
            # Stop tracing without saving a ZIP for passed scenarios.
            context.browser_context.tracing.stop()
            trace_stopped = True

    finally:
        # Make sure tracing is stopped if an earlier operation failed.
        if not trace_stopped:
            try:
                context.browser_context.tracing.stop()
            except Exception:
                pass

        # Close the browser context to finalize the video.
        try:
            context.browser_context.close()
        except Exception as error:
            print(f"Browser context cleanup failed: {error}")

    # Attach the finalized video after closing the context.
    if video is not None:
        try:
            video_path = video.path()

            allure.attach.file(
                str(video_path),
                name=f"{scenario.name} - Video",
                attachment_type="video/webm",
                extension="webm"
            )

            print(f"Video saved: {video_path}")

        except Exception as error:
            print(f"Video attachment failed: {error}")

    print(f"Scenario status: {scenario.status}")


def after_all(context):

    # Close the browser after all scenarios finish.
    try:
        context.browser.close()
    finally:
        # Stop Playwright even if browser cleanup encounters an error.
        context.playwright.stop()

    print("\nPlaywright browser closed successfully!")
