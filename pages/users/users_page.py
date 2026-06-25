import re
import logging

from playwright.sync_api import expect, Page

from pages.common.base_page import BasePage
from utils.waits import SHORT, DEFAULT, LONG, LOAD

logger = logging.getLogger(__name__)


class UsersPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.users_menu          = page.get_by_role("link", name="Users")
        # Two separate "Create User" elements:
        #   toolbar_create_user_btn  → opens the popup (always enabled)
        #   submit button inside popup → disabled until form is filled
        self.create_user_btn = page.get_by_role(
            "button", name="Create User"
        ).first   # toolbar button — always first in DOM order
        self.change_status_btn   = page.get_by_role("button", name="Change Status")
        self.users_heading       = page.get_by_role("heading", name="Users")
        self.create_user_heading = page.get_by_role("heading", name="Create User")

    # =========================================================================
    # PRIVATE
    # =========================================================================

    def _reload_users_page(self) -> None:
        self.page.reload()
        self.wait.for_url_contains("/users", timeout=LOAD)
        expect(self.users_heading).to_be_visible(timeout=DEFAULT)

    def _role_option(self, role: str):
        label = self.page.locator("[data-floating-ui-portal]").get_by_text(
            role, exact=True
        )
        if label.count() == 0:
            label = self.page.get_by_text(role, exact=True)
        return label.first.locator("xpath=..")

    def _user_row(self, identifier: str):
        return self.page.get_by_role(
            "row", name=re.compile(re.escape(identifier))
        )

    # =========================================================================
    # OPEN USERS PAGE
    # =========================================================================

    def open_users_page(self) -> None:
        self.safe_click(self.users_menu)
        self.wait.for_url_contains("/users", timeout=LOAD)
        expect(self.users_heading).to_be_visible(timeout=DEFAULT)
        logger.info("[UsersPage] Users page opened")

    # =========================================================================
    # ASSERTIONS
    # =========================================================================

    def verify_users_page_opened(self) -> None:
        expect(self.page).to_have_url(
            re.compile(r"/users$"), timeout=LONG
        )
        self.verify_visible(self.users_heading, timeout=LONG)
        logger.info(f"[UsersPage]  Users page verified: {self.page.url}")

    def verify_create_user_popup_open(self) -> None:
        self.verify_visible(self.create_user_heading, timeout=DEFAULT)
        logger.info("[UsersPage]  Create User popup is open")

    def verify_create_user_popup_closed(self) -> None:
        self.verify_hidden(self.create_user_heading, timeout=DEFAULT)
        logger.info("[UsersPage]  Create User popup closed")

    def verify_create_button_enabled(self) -> None:
        # Scoped to dialog — toolbar "Create User" is always enabled and
        # would make this assertion meaningless if matched instead
        dialog = self.page.get_by_role("dialog")
        create_btn = dialog.get_by_role("button", name="Create User")
        self.verify_enabled(create_btn, timeout=DEFAULT)
        logger.info("[UsersPage]  Create User button is enabled")

    def verify_user_in_list(self, identifier: str) -> None:
        self.verify_visible(self._user_row(identifier).first, timeout=LONG)
        logger.info(f"[UsersPage]  User visible in list: {identifier}")

    def verify_change_status_disabled(self) -> None:
        self.verify_disabled(self.change_status_btn, timeout=DEFAULT)
        logger.info("[UsersPage]  Change Status button is disabled")

    def verify_change_status_enabled(self) -> None:
        self.verify_enabled(self.change_status_btn, timeout=DEFAULT)
        logger.info("[UsersPage]  Change Status button is enabled")

    def verify_status_option_visible(self, option: str) -> None:
        self.verify_visible(
            self.page.get_by_role("button", name=option, exact=True).first,
            timeout=DEFAULT
        )
        logger.info(f"[UsersPage]  Status option visible: {option}")

    def verify_both_status_options_visible(self) -> None:
        self.verify_visible(
            self.page.get_by_role("button", name="Activate", exact=True).nth(0),
            timeout=DEFAULT
        )
        self.verify_visible(
            self.page.get_by_role("button", name="Deactivate", exact=True).nth(0),
            timeout=DEFAULT
        )
        logger.info("[UsersPage]  Both Activate and Deactivate options visible")

    def verify_user_status(self, identifier: str, expected_status: str) -> None:
        expect(
            self._user_row(identifier).first.get_by_text(expected_status)
        ).to_be_visible(timeout=LONG)
        logger.info(
            f"[UsersPage]  User status verified: {identifier} → {expected_status}"
        )

    def verify_user_still_in_list(self, identifier: str) -> None:
        self.verify_visible(self._user_row(identifier).first, timeout=LONG)
        logger.info(
            f"[UsersPage]  User still in list after status change: {identifier}"
        )

    # =========================================================================
    # CREATE USER
    # =========================================================================

    def create_user(
        self,
        full_name: str,
        email: str,
        password: str,
        roles: list
    ) -> None:
        self.safe_click(self.create_user_btn)
        expect(self.create_user_heading).to_be_visible(timeout=DEFAULT)
        logger.info("[UsersPage] Create User popup opened")

        self.safe_fill(
            self.page.get_by_role("textbox", name="Enter Full Name"), full_name
        )
        self.safe_fill(
            self.page.get_by_role("textbox", name="Enter Email"), email
        )
        self.safe_fill(
            self.page.get_by_role("textbox", name="Enter Password"), password
        )
        self.safe_fill(
            self.page.get_by_role("textbox", name="Confirm Password"), password
        )
        logger.info(f"[UsersPage] Credentials filled for: {full_name}")

        roles_dropdown = self.page.get_by_role("button", name="Select roles")
        self.safe_click(roles_dropdown)
        self.wait.for_visible(self._role_option(roles[0]), timeout=DEFAULT)

        for role in roles:
            self.safe_click(self._role_option(role))
            logger.info(f"[UsersPage] Role selected: {role}")

        self.page.mouse.click(50, 50)
        try:
            self.wait.for_hidden(
                self.page.locator(
                    "[data-floating-ui-portal], [role='listbox']"
                ).first,
                timeout=SHORT,
            )
        except Exception:
            pass

        dialog = self.page.get_by_role("dialog")
        self.safe_click(
            dialog.get_by_role("button", name="Create User")
        )
        logger.info(f"[UsersPage] Create User clicked for: {full_name}")

        # Best-effort toast + error detection
        try:
            expect(self.page.get_by_text("User created")).to_be_visible(
                timeout=SHORT
            )
            logger.info("[UsersPage] User creation toast verified")
        except Exception:
            error_toast = self.page.get_by_text(
                re.compile("already exists|error|failed", re.I)
            )
            if error_toast.count() > 0 and error_toast.first.is_visible():
                raise AssertionError(
                    f"User creation FAILED for {email}: "
                    f"{error_toast.first.inner_text()}"
                )

        expect(
            self._user_row(email).first
        ).to_be_visible(timeout=LONG)
        logger.info(f"[UsersPage] User added to list: {email}")

    # =========================================================================
    # SINGLE USER STATUS CHANGE
    # =========================================================================

    def change_single_user_status(
        self,
        user_identifier: str,
        action: str,
        expected_status: str
    ) -> None:
        user_row = self._user_row(user_identifier)
        user_row.get_by_role("checkbox").check()
        logger.info(f"[UsersPage] User selected: {user_identifier}")

        expect(self.change_status_btn).to_be_enabled(timeout=DEFAULT)
        self.safe_click(self.change_status_btn)

        action_button = self.page.get_by_role("button", name=action)
        expect(action_button).to_be_visible(timeout=DEFAULT)
        self.safe_click(action_button)
        logger.info(f"[UsersPage] Status action clicked: {action}")

        self._reload_users_page()

        expect(
            self._user_row(user_identifier).first.get_by_text(expected_status)
        ).to_be_visible(timeout=LONG)
        logger.info(
            f"[UsersPage] Status verified: {user_identifier} → {expected_status}"
        )

    # =========================================================================
    # BULK STATUS CHANGE
    # =========================================================================

    def bulk_change_status(
        self,
        user_identifiers: list,
        action: str,
        expected_status: str
    ) -> None:
        for user in user_identifiers:
            self._user_row(user).get_by_role("checkbox").check()
            logger.info(f"[UsersPage] User selected for bulk: {user}")

        expect(self.change_status_btn).to_be_enabled(timeout=DEFAULT)
        self.safe_click(self.change_status_btn)

        expect(
            self.page.get_by_role("button", name="Activate", exact=True).nth(0)
        ).to_be_visible(timeout=DEFAULT)
        expect(
            self.page.get_by_role("button", name="Deactivate", exact=True).nth(0)
        ).to_be_visible(timeout=DEFAULT)
        logger.info("[UsersPage] Both Activate and Deactivate options visible")

        self.safe_click(
            self.page.get_by_role("button", name=action, exact=True).nth(0)
        )
        logger.info(f"[UsersPage] Bulk action clicked: {action}")

        self._reload_users_page()

        for user in user_identifiers:
            expect(
                self._user_row(user).first.get_by_text(expected_status)
            ).to_be_visible(timeout=LONG)
            logger.info(
                f"[UsersPage] Bulk status verified: {user} → {expected_status}"
            )