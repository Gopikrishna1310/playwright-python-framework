import os
import time
import pytest

from playwright.sync_api import (
    sync_playwright
)

# ============================================
# CREATE SCREENSHOTS DIRECTORY
# ============================================

os.makedirs(
    "screenshots",
    exist_ok=True
)

# ============================================
# PLAYWRIGHT PAGE FIXTURE
# ============================================

@pytest.fixture
def page():

    with sync_playwright() as p:

        # ============================================
        # LAUNCH BROWSER
        # ============================================

        browser = p.chromium.launch(
            headless=False,
            slow_mo=300
        )

        # ============================================
        # CREATE CONTEXT
        # ============================================

        context = browser.new_context(

            permissions=[
                "clipboard-read",
                "clipboard-write"
            ],

            viewport={
                "width": 1536,
                "height": 864
            }
        )

        # ============================================
        # GLOBAL TIMEOUTS
        # ============================================

        context.set_default_timeout(
            30000
        )

        context.set_default_navigation_timeout(
            60000
        )

        # ============================================
        # CREATE PAGE
        # ============================================

        page = context.new_page()

        # ============================================
        # MAXIMIZE WINDOW
        # ============================================

        page.set_viewport_size({
            "width": 1536,
            "height": 864
        })

        yield page

        # ============================================
        # CLEANUP
        # ============================================

        context.close()

        browser.close()


# ============================================
# SCREENSHOT ON FAILURE
# ============================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item,
    call
):

    outcome = yield

    report = outcome.get_result()

    # ============================================
    # TAKE SCREENSHOT ONLY ON FAILURE
    # ============================================

    if (
        report.when == "call"
        and report.failed
    ):

        page = item.funcargs.get(
            "page"
        )

        if page:

            screenshot_name = (
                f"screenshots/"
                f"failure_{int(time.time())}.png"
            )

            page.screenshot(
                path=screenshot_name,
                full_page=True
            )

            print(
                f"\n📸 Screenshot saved: "
                f"{screenshot_name}"
            )