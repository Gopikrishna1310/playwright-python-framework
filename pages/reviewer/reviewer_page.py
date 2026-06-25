import re
import logging

from playwright.sync_api import expect, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from config.urls import BASE_URL
from pages.common.base_page import BasePage
from utils.waits import SHORT, DEFAULT, LONG

logger = logging.getLogger(__name__)


class ReviewerPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # =========================================================================
    # PRIVATE
    # =========================================================================

    def _dialog(self):
        dialog = self.page.get_by_role("dialog")
        try:
            self.wait.for_visible(dialog.first, timeout=DEFAULT)
            return dialog.first
        except (PlaywrightTimeoutError, AssertionError):
            return self.page

    # =========================================================================
    # OPEN LOGIN PAGE
    # =========================================================================

    def open_login_page(self) -> None:
        self.page.context.grant_permissions(["microphone"], origin=BASE_URL)
        self.page.goto(f"{BASE_URL}/login")

    # =========================================================================
    # LOGIN
    # =========================================================================

    def login(self, email: str, password: str) -> None:
        self.safe_fill(self.page.get_by_role("textbox", name="Email"), email)
        self.safe_fill(self.page.get_by_role("textbox", name="Password"), password)
        self.safe_click(self.page.get_by_role("button", name="Sign in"))
        logger.info("[ReviewerPage] Login submitted")

    # =========================================================================
    # SELECT ORGANIZATION & ROLE
    # =========================================================================

    def select_organization_and_role(self) -> None:
        org_locator = self.page.locator("div").filter(
            has_text=re.compile(r"^ObjectwaysYour roles:")
        ).nth(4)
        self.safe_click(org_locator)
        logger.info("[ReviewerPage] Organisation selected")

        role_locator = self.page.locator("div").filter(
            has_text=re.compile(r"^Reviewer$")
        ).nth(1)
        self.wait.for_visible(role_locator, timeout=DEFAULT)
        self.safe_click(role_locator)
        logger.info("[ReviewerPage] Reviewer role selected")

        continue_button = self.page.get_by_role("button", name="Continue")
        self.wait.for_visible(continue_button, timeout=DEFAULT)
        self.safe_click(continue_button)
        logger.info("[ReviewerPage] Continue clicked")

    # =========================================================================
    # VALIDATE REVIEWER LOGIN
    # =========================================================================

    def validate_reviewer_login(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*/tasks"), timeout=LONG)
        expect(self.page.get_by_role("link", name="Home")).to_be_visible(timeout=LONG)
        expect(self.page.get_by_role("link", name="Tasks")).to_be_visible(timeout=LONG)
        logger.info("[ReviewerPage] Reviewer redirected to Tasks page")

    # =========================================================================
    # OPEN TASK
    # =========================================================================

    def open_task(self, task_name: str) -> None:
        cell = self.page.get_by_role("cell", name=task_name).first
        self.wait.for_visible(cell, timeout=LONG)
        self.safe_click(cell)

        claim_button = self.page.get_by_role("button", name="Claim Task")
        iframe       = self.page.locator("iframe").first
        self.wait.for_visible(claim_button.or_(iframe), timeout=LONG)
        logger.info(f"[ReviewerPage] Task opened: {task_name}")

    # =========================================================================
    # CLAIM TASK
    # =========================================================================

    def claim_task(self) -> None:
        claim_button = self.page.get_by_role("button", name="Claim Task")
        self.wait.for_visible(claim_button, timeout=LONG)
        self.safe_click(claim_button)
        logger.info("[ReviewerPage] Task claimed")

    # =========================================================================
    # CLOSE COMMENTS POPUP
    # =========================================================================

    def close_comments_popup(self) -> None:
        try:
            comments_dialog = self.page.get_by_role("dialog")
            self.wait.for_visible(comments_dialog.first, timeout=5_000)
            close_button = comments_dialog.first.get_by_role("button").last
            self.safe_click(close_button)
            self.wait.for_hidden(comments_dialog.first, timeout=DEFAULT)
            logger.info("[ReviewerPage] Comments popup closed")
        except (PlaywrightTimeoutError, AssertionError):
            logger.info("[ReviewerPage] No Comments popup found — continuing")

    # =========================================================================
    # REJECT TASK
    # =========================================================================

    def reject_task(self, comment: str) -> None:
        self.safe_click(self.page.get_by_role("button", name="Reject"))
        logger.info("[ReviewerPage] Reject popup opened")

        dialog      = self._dialog()
        comment_box = dialog.get_by_role("textbox")

        try:
            self.wait.for_visible(comment_box, timeout=DEFAULT)
            self.safe_fill(comment_box, comment)
            logger.info(f"[ReviewerPage] Reject comment entered: {comment}")
        except (PlaywrightTimeoutError, AssertionError):
            logger.info("[ReviewerPage] No comment box — continuing without comment")

        self.safe_click(dialog.get_by_role("button", name="Submit"))
        logger.info("[ReviewerPage] Task rejected")

        try:
            self.wait.for_hidden(
                self.page.locator("div[role='dialog']"), timeout=SHORT
            )
        except (PlaywrightTimeoutError, AssertionError):
            pass

    # =========================================================================
    # OPEN PROFILE MENU
    # =========================================================================

    def open_profile_menu(self) -> None:
        self.safe_click(
            self.page.locator("div").filter(
                has_text=re.compile(r"^R$")
            ).nth(2)
        )
        logger.info("[ReviewerPage] Profile menu opened")

    # =========================================================================
    # LOGOUT
    # =========================================================================

    def logout(self) -> None:
        logout_button = self.page.get_by_role("button", name="Logout")
        self.wait.for_visible(logout_button, timeout=DEFAULT)
        self.safe_click(logout_button)
        expect(self.page).to_have_url(re.compile(r".*/login"), timeout=LONG)
        logger.info("[ReviewerPage] Reviewer logout successful")

    # =========================================================================
    # APPROVE TASK
    # =========================================================================

    def approve_task(self) -> None:
        approve_button = self.page.get_by_role("button", name="Approve")

        self.safe_click(approve_button)
        logger.info("[ReviewerPage] Approve confirmation popup opened")

        self.page.once("dialog", lambda dialog: dialog.accept())
        self.safe_click(approve_button)

        try:
            self.wait.for_page_ready()
        except (PlaywrightTimeoutError, AssertionError):
            pass

        self.page.once("dialog", lambda dialog: dialog.accept())

        try:
            self.wait.for_page_ready()
        except (PlaywrightTimeoutError, AssertionError):
            pass

        logger.info("[ReviewerPage] Task approved")