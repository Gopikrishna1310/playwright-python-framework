import re
import time
import logging
from playwright.sync_api import Page, Locator, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from utils.waits import SmartWait, DEFAULT, LONG, LOAD

logger = logging.getLogger(__name__)


class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.wait = SmartWait(page)

    # =========================================================================
    # NAVIGATION
    # =========================================================================

    def open_url(self, url: str) -> None:
        logger.info(f"[Navigation] Opening: {url}")
        self.page.goto(url, wait_until="domcontentloaded", timeout=LOAD)
        self.wait.for_page_ready()

    # =========================================================================
    # CLICK ACTIONS
    # =========================================================================

    def safe_click(self, locator: Locator, timeout: int = DEFAULT) -> None:
        try:
            locator.click(timeout=timeout)
        except PlaywrightTimeoutError:
            logger.error(f"[BasePage] safe_click failed after {timeout}ms → {locator}")
            raise

    def safe_click_with_wait(
        self, locator: Locator, wait_url: str = None, timeout: int = DEFAULT
    ) -> None:
        self.safe_click(locator, timeout=timeout)
        if wait_url:
            self.wait.for_url_contains(wait_url, timeout=LOAD)
        else:
            self.wait.for_page_ready()

    def safe_double_click(self, locator: Locator, timeout: int = DEFAULT) -> None:
        try:
            locator.dbl_click(timeout=timeout)
        except PlaywrightTimeoutError:
            logger.error(f"[BasePage] safe_double_click failed after {timeout}ms")
            raise

    # =========================================================================
    # FILL / TYPE ACTIONS
    # =========================================================================

    def safe_fill(self, locator: Locator, text: str, timeout: int = DEFAULT) -> None:
        try:
            locator.clear(timeout=timeout)
            locator.fill(text, timeout=timeout)
        except PlaywrightTimeoutError:
            logger.error(f"[BasePage] safe_fill failed after {timeout}ms → {locator}")
            raise

    def safe_type(self, locator: Locator, text: str, delay: int = 50) -> None:
        """Use when fill() doesn't trigger JS listeners (autocomplete, input masks)."""
        locator.click()
        locator.clear()
        locator.press_sequentially(text, delay=delay)

    # =========================================================================
    # SELECT / CHECKBOX / HOVER
    # =========================================================================

    def safe_select(self, locator: Locator, value: str = None, label: str = None, timeout: int = DEFAULT) -> None:
        self.wait.for_visible(locator, timeout=timeout)
        if label:
            locator.select_option(label=label)
        else:
            locator.select_option(value)

    def safe_hover(self, locator: Locator, timeout: int = DEFAULT) -> None:
        self.wait.for_visible(locator, timeout=timeout)
        locator.hover()

    def safe_check(self, locator: Locator, timeout: int = DEFAULT) -> None:
        locator.check(timeout=timeout)

    def safe_uncheck(self, locator: Locator, timeout: int = DEFAULT) -> None:
        locator.uncheck(timeout=timeout)

    def press_key(self, key: str) -> None:
        self.page.keyboard.press(key)

    # =========================================================================
    # CLIPBOARD
    # =========================================================================

    def read_clipboard(self, expected_prefix: str = None, timeout: int = 10_000) -> str:
        """Polls clipboard after a copy action until real data lands."""
        deadline = time.time() + (timeout / 1000)
        last = ""
        while time.time() < deadline:
            last = self.page.evaluate("navigator.clipboard.readText()") or ""
            if last.strip():
                if expected_prefix is None or last.strip().startswith(expected_prefix):
                    return last.strip()
            self.page.wait_for_timeout(150)
        raise TimeoutError(
            f"[BasePage] Clipboard not ready after {timeout}ms "
            f"(expected_prefix={expected_prefix!r}, last seen={last[:40]!r})"
        )

    # =========================================================================
    # WAIT HELPERS
    # =========================================================================

    def wait_for_element(self, locator: Locator, timeout: int = DEFAULT) -> None:
        self.wait.for_visible(locator, timeout=timeout)

    def wait_for_element_gone(self, locator: Locator, timeout: int = DEFAULT) -> None:
        self.wait.for_hidden(locator, timeout=timeout)

    def wait_for_page_load(self) -> None:
        self.wait.for_page_ready()

    def wait_for_url(self, partial_url: str, timeout: int = LOAD) -> None:
        self.wait.for_url_contains(partial_url, timeout=timeout)

    def wait_for_spinner(self, spinner_locator: Locator, timeout: int = LONG) -> None:
        self.wait.for_spinner_gone(spinner_locator, timeout=timeout)

    # =========================================================================
    # ASSERTIONS
    # =========================================================================

    def verify_visible(self, locator: Locator, timeout: int = DEFAULT) -> None:
        expect(locator).to_be_visible(timeout=timeout)

    def verify_hidden(self, locator: Locator, timeout: int = DEFAULT) -> None:
        expect(locator).to_be_hidden(timeout=timeout)

    def verify_text(self, locator: Locator, expected_text: str, timeout: int = DEFAULT) -> None:
        expect(locator).to_have_text(expected_text, timeout=timeout)

    def verify_contains_text(self, locator: Locator, text: str, timeout: int = DEFAULT) -> None:
        expect(locator).to_contain_text(text, timeout=timeout)

    def verify_url(self, partial_url: str, timeout: int = DEFAULT) -> None:
        expect(self.page).to_have_url(
            re.compile(re.escape(partial_url)), timeout=timeout
        )

    def verify_enabled(self, locator: Locator, timeout: int = DEFAULT) -> None:
        expect(locator).to_be_enabled(timeout=timeout)

    def verify_disabled(self, locator: Locator, timeout: int = DEFAULT) -> None:
        expect(locator).to_be_disabled(timeout=timeout)

    def verify_count(self, locator: Locator, count: int, timeout: int = DEFAULT) -> None:
        expect(locator).to_have_count(count, timeout=timeout)

    # =========================================================================
    # GETTERS
    # =========================================================================

    def get_text(self, locator: Locator, timeout: int = DEFAULT) -> str:
        self.wait.for_visible(locator, timeout=timeout)
        return locator.text_content().strip()

    def get_attribute(self, locator: Locator, attribute: str, timeout: int = DEFAULT) -> str:
        self.wait.for_visible(locator, timeout=timeout)
        return locator.get_attribute(attribute)

    def get_input_value(self, locator: Locator, timeout: int = DEFAULT) -> str:
        self.wait.for_visible(locator, timeout=timeout)
        return locator.input_value()

    def is_visible(self, locator: Locator) -> bool:
        """Returns True/False — does NOT fail the test."""
        return locator.is_visible()

    def is_enabled(self, locator: Locator) -> bool:
        """Returns True/False — does NOT fail the test."""
        return locator.is_enabled()

    # =========================================================================
    # SCROLL
    # =========================================================================

    def scroll_into_view(self, locator: Locator) -> None:
        locator.scroll_into_view_if_needed()

    def scroll_to_bottom(self) -> None:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self) -> None:
        self.page.evaluate("window.scrollTo(0, 0)")

    # =========================================================================
    # TAB / WINDOW HANDLING
    # =========================================================================

    def switch_to_page(self, page: Page) -> None:
        page.bring_to_front()
        page.wait_for_load_state("domcontentloaded", timeout=LOAD)
        try:
            page.wait_for_load_state("networkidle", timeout=8_000)
        except PlaywrightTimeoutError:
            logger.warning("[BasePage] networkidle not reached on tab switch — continuing")

    def open_new_tab(self, trigger_locator: Locator) -> Page:
        return self.wait.for_new_tab(lambda: trigger_locator.click())