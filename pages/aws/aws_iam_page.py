import logging

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.common.base_page import BasePage
from utils.waits import DEFAULT, LONG, LOAD

logger = logging.getLogger(__name__)


class AWSIAMPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.policy_search = self.page.get_by_role("searchbox", name="Search items")

    # =========================================================================
    # OPEN IAM CONSOLE
    # =========================================================================

    def open_iam_console(self) -> None:
        self.page.goto(
            "https://us-east-1.console.aws.amazon.com/iam/home",
            wait_until="domcontentloaded",
            timeout=LOAD,
        )
        self.wait.for_url_contains("/iam/home", timeout=LONG)
        self.wait.for_page_ready()
        logger.info("[AWSIAMPage] IAM console opened")

    # =========================================================================
    # OPEN POLICIES PAGE
    # =========================================================================

    def open_policies_page(self) -> None:
        self.safe_click(self.page.get_by_role("link", name="Policies", exact=True))
        self.wait.for_visible(self.policy_search, timeout=LONG)
        logger.info("[AWSIAMPage] Policies page opened")

    # =========================================================================
    # SEARCH POLICY
    # =========================================================================

    def search_policy(self, policy_name: str) -> None:
        self.safe_fill(self.policy_search, policy_name)
        logger.info(f"[AWSIAMPage] Searching policy: {policy_name}")

    # =========================================================================
    # OPEN POLICY
    # =========================================================================

    def open_policy(self, policy_name: str) -> None:
        policy_link = self.page.get_by_role("link", name=policy_name).first
        self.wait.for_visible(policy_link, timeout=LONG)
        self.safe_click(policy_link)
        self.wait.for_visible(
            self.page.get_by_role("button", name="Edit policy permissions").first,
            timeout=LONG,
        )
        logger.info(f"[AWSIAMPage] Policy opened: {policy_name}")

    # =========================================================================
    # CLICK EDIT POLICY
    # =========================================================================

    def click_edit_policy(self) -> None:
        self.safe_click(
            self.page.get_by_role("button", name="Edit policy permissions").first
        )

        json_tab = self.page.get_by_role("tab", name="JSON")
        try:
            self.wait.for_visible(json_tab, timeout=5_000)
            self.safe_click(json_tab)
            logger.info("[AWSIAMPage] Switched to JSON tab")
        except (PlaywrightTimeoutError, AssertionError):
            logger.info("[AWSIAMPage] JSON tab not shown — editor already in JSON mode")

        self.wait.for_visible(self.page.locator(".ace_content"), timeout=LONG)
        logger.info("[AWSIAMPage] Policy JSON editor ready")

    # =========================================================================
    # REPLACE POLICY JSON
    # =========================================================================

    def replace_policy_json(self, policy_json: str) -> None:
        editor = self.page.locator(".ace_content")
        self.wait.for_visible(editor, timeout=LONG)
        editor.click(force=True)
        self.page.keyboard.press("Control+A")
        self.page.keyboard.press("Backspace")
        self.page.keyboard.insert_text(policy_json)
        self.verify_contains_text(editor, "Statement", timeout=DEFAULT)
        logger.info("[AWSIAMPage] Policy JSON replaced")

    # =========================================================================
    # SAVE POLICY
    # =========================================================================

    def save_policy(self) -> None:
        advanced = False
        for label in ["Next", "Review policy", "Save changes"]:
            candidate = self.page.get_by_role("button", name=label).first
            if candidate.is_visible():
                self.safe_click(candidate)
                advanced = True
                logger.info(f"[AWSIAMPage] Advanced via '{label}' button")
                break

        if not advanced:
            raise RuntimeError(
                "[AWSIAMPage] save_policy(): No advance button found."
            )

        confirm_save = self.page.get_by_role("button", name="Save changes").last
        try:
            self.wait.for_visible(confirm_save, timeout=15_000)
            self.safe_click(confirm_save)
            logger.info("[AWSIAMPage] Final save confirmation clicked")
        except (PlaywrightTimeoutError, AssertionError):
            logger.info("[AWSIAMPage] No second confirmation — single-step save")

        self.wait.for_url_not_contains("/edit", timeout=LONG)
        logger.info("[AWSIAMPage] Policy saved — URL left /edit")