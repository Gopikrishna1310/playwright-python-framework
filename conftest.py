import os
import logging
import pytest

from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

os.makedirs("screenshots", exist_ok=True)
os.makedirs("reports",     exist_ok=True)

DEFAULT_TIMEOUT    = 30_000
NAVIGATION_TIMEOUT = 60_000
SLOW_MO            = int(os.getenv("SLOW_MO", "0"))


@pytest.fixture
def page():
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=SLOW_MO,
        )

        context = browser.new_context(
            permissions=["clipboard-read", "clipboard-write"],
            viewport={"width": 1536, "height": 864},
            ignore_https_errors=True
        )

        context.set_default_timeout(DEFAULT_TIMEOUT)
        context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)

        logger.info(
            f"[conftest] Browser ready | "
            f"timeout={DEFAULT_TIMEOUT}ms | "
            f"nav_timeout={NAVIGATION_TIMEOUT}ms | "
            f"slow_mo={SLOW_MO}ms"
        )

        page = context.new_page()
        page.set_viewport_size({"width": 1536, "height": 864})

        yield page

        context.close()
        browser.close()
        logger.info("[conftest] Browser closed — cleanup complete")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report  = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            safe_test_name = (
                item.name
                .replace("/",  "_")
                .replace("\\", "_")
                .replace(":",  "_")
                .replace(" ",  "_")
            )
            screenshot_path = f"screenshots/{safe_test_name}__failure.png"
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"[conftest]  Screenshot saved → {screenshot_path}")
            except Exception as e:
                logger.warning(f"[conftest] Could not save screenshot for '{item.name}': {e}")