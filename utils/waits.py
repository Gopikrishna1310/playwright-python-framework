import logging
from playwright.sync_api import Page, Locator, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

# Timeouts are CEILINGS not sleeps — tests return the moment condition is met
SHORT   =  5_000   #  5s — near-instant operations (redirects, DOM already present)
DEFAULT = 30_000   # 30s — standard network-dependent operations
LONG    = 60_000   # 60s — heavy operations: file upload, slow APIs
LOAD    = 45_000   # 45s — full page loads and navigations


class SmartWait:

    def __init__(self, page: Page):
        self.page = page

    # =========================================================================
    # ELEMENT WAITS
    # =========================================================================

    def for_visible(self, locator: Locator, timeout: int = DEFAULT) -> None:
        try:
            locator.wait_for(state="visible", timeout=timeout)
        except PlaywrightTimeoutError:
            logger.error(f"[SmartWait] Element not visible after {timeout}ms → {locator}")
            raise

    def for_hidden(self, locator: Locator, timeout: int = DEFAULT) -> None:
        try:
            locator.wait_for(state="hidden", timeout=timeout)
        except PlaywrightTimeoutError:
            logger.error(f"[SmartWait] Element still visible after {timeout}ms → {locator}")
            raise

    def for_spinner_gone(self, spinner_locator: Locator, timeout: int = LONG) -> None:
        try:
            if spinner_locator.is_visible():
                spinner_locator.wait_for(state="hidden", timeout=timeout)
        except PlaywrightTimeoutError:
            logger.error(f"[SmartWait] Spinner still visible after {timeout}ms")
            raise

    def for_clickable(self, locator: Locator, timeout: int = DEFAULT) -> None:
        """Use only when you need to CHECK readiness before clicking — click() already auto-waits."""
        try:
            locator.wait_for(state="visible", timeout=timeout)
            expect(locator).to_be_enabled(timeout=timeout)
        except (PlaywrightTimeoutError, AssertionError):
            logger.error(f"[SmartWait] Element not clickable after {timeout}ms → {locator}")
            raise

    def for_text_in_element(self, locator: Locator, text: str, timeout: int = DEFAULT) -> None:
        try:
            expect(locator).to_contain_text(text, timeout=timeout)
        except AssertionError:
            logger.error(f"[SmartWait] Text '{text}' not found after {timeout}ms")
            raise

    def for_exact_text(self, locator: Locator, text: str, timeout: int = DEFAULT) -> None:
        try:
            expect(locator).to_have_text(text, timeout=timeout)
        except AssertionError:
            logger.error(f"[SmartWait] Exact text '{text}' not found after {timeout}ms")
            raise

    def for_count(self, locator: Locator, count: int, timeout: int = DEFAULT) -> None:
        try:
            expect(locator).to_have_count(count, timeout=timeout)
        except AssertionError:
            logger.error(f"[SmartWait] Expected {count} elements, not found after {timeout}ms")
            raise

    def for_input_value(self, locator: Locator, value: str, timeout: int = DEFAULT) -> None:
        try:
            expect(locator).to_have_value(value, timeout=timeout)
        except AssertionError:
            logger.error(f"[SmartWait] Input value '{value}' not found after {timeout}ms")
            raise

    # =========================================================================
    # PAGE / NAVIGATION WAITS
    # =========================================================================

    def for_page_ready(self, timeout: int = LOAD) -> None:
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except PlaywrightTimeoutError:
            logger.warning("[SmartWait] networkidle not reached — continuing after domcontentloaded")

    def for_url_contains(self, partial_url: str, timeout: int = LOAD) -> None:
        try:
            self.page.wait_for_url(f"**{partial_url}**", timeout=timeout)
        except PlaywrightTimeoutError:
            logger.error(
                f"[SmartWait] URL did not contain '{partial_url}' after {timeout}ms. "
                f"Current URL: {self.page.url}"
            )
            raise

    def for_url_exact(self, full_url: str, timeout: int = LOAD) -> None:
        try:
            self.page.wait_for_url(full_url, timeout=timeout)
        except PlaywrightTimeoutError:
            logger.error(
                f"[SmartWait] URL did not match '{full_url}' after {timeout}ms. "
                f"Current URL: {self.page.url}"
            )
            raise

    def for_url_not_contains(self, partial_url: str, timeout: int = LOAD) -> None:
        try:
            self.page.wait_for_url(lambda url: partial_url not in url, timeout=timeout)
        except PlaywrightTimeoutError:
            logger.error(
                f"[SmartWait] URL still contains '{partial_url}' after {timeout}ms. "
                f"Current: {self.page.url}"
            )
            raise

    # =========================================================================
    # ADVANCED WAITS
    # =========================================================================

    def for_api_response(self, url_pattern: str, timeout: int = LONG):
        try:
            return self.page.expect_response(
                lambda response: url_pattern in response.url and response.status == 200,
                timeout=timeout,
            )
        except PlaywrightTimeoutError:
            logger.error(f"[SmartWait] API response for '{url_pattern}' not received after {timeout}ms")
            raise

    def for_download(self, trigger_action, timeout: int = LONG):
        try:
            with self.page.expect_download(timeout=timeout) as download_info:
                trigger_action()
            return download_info.value
        except PlaywrightTimeoutError:
            logger.error(f"[SmartWait] Download did not start after {timeout}ms")
            raise

    def for_new_tab(self, trigger_action, timeout: int = DEFAULT) -> Page:
        try:
            with self.page.context.expect_page(timeout=timeout) as new_page_info:
                trigger_action()
            new_page = new_page_info.value
            new_page.wait_for_load_state("domcontentloaded", timeout=timeout)
            return new_page
        except PlaywrightTimeoutError:
            logger.error(f"[SmartWait] New tab did not open after {timeout}ms")
            raise