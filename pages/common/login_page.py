import re
import logging
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.common.base_page import BasePage
from utils.waits import SHORT, DEFAULT, LONG

logger = logging.getLogger(__name__)

LOGIN_URL     = "https://fmn-qa.tensoract.com/login"
DASHBOARD_URL = "https://fmn-qa.tensoract.com/"


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.email_input       = page.get_by_role("textbox", name="Email")
        self.password_input    = page.get_by_role("textbox", name="Password")
        self.sign_in_button    = page.get_by_role("button",  name="Sign in", exact=True)
        self.organization_card = page.get_by_role("heading", name="Objectways")
        self.company_admin_role = page.get_by_role("paragraph").filter(
            has_text=re.compile(r"^Company Admin$")
        )
        self.continue_button   = page.get_by_role("button", name="Continue")
        self.welcome_heading   = page.get_by_role("heading", name="Welcome to Tensoract")
        self.home_sidebar_link = page.get_by_role("link", name="Home")

    # =========================================================================
    # OPEN LOGIN PAGE
    # =========================================================================

    def open_login_page(self) -> None:
        self.open_url(LOGIN_URL)
        logger.info("[LoginPage] Login page opened")

    # =========================================================================
    # STEP METHODS
    # =========================================================================

    def clear_credentials(self) -> None:
        self.email_input.clear()
        self.password_input.clear()
        logger.info("[LoginPage] Credentials cleared")

    def enter_credentials(self, username: str, password: str) -> None:
        logger.info(f"[LoginPage] Entering credentials for: {username}")
        self.safe_fill(self.email_input, username)
        self.safe_fill(self.password_input, password)
        self.safe_click(self.sign_in_button)
        self.wait.for_page_ready()
        logger.info("[LoginPage] Sign In clicked")

    def select_organization(self) -> None:
        self.safe_click(self.organization_card, timeout=15000)
        logger.info("[LoginPage] Organisation 'Objectways' clicked")

    def select_role(self) -> None:
        self.safe_click(self.company_admin_role)
        logger.info("[LoginPage] Role 'Company Admin' clicked")

    def click_continue(self) -> None:
        self.safe_click(self.continue_button)
        self.wait.for_url_exact(DASHBOARD_URL, timeout=SHORT)
        logger.info("[LoginPage] Continue clicked — redirected to dashboard")

    # =========================================================================
    # LOGIN  (convenience method for other test files)
    # =========================================================================

    def login(self, username: str, password: str) -> None:
        """Full login flow in one call. Use in other modules where login
        is a prerequisite, not the thing being tested."""
        logger.info(f"[LoginPage] Starting login for: {username}")
        self.enter_credentials(username, password)
        try:
            self.select_organization()
            self.select_role()
            self.click_continue()
        except PlaywrightTimeoutError:
            logger.info("[LoginPage] Organisation screen not shown — already on dashboard")
        logger.info("[LoginPage] Login complete")

    # =========================================================================
    # ASSERTIONS
    # =========================================================================

    def verify_org_selection_visible(self) -> None:
        self.verify_visible(self.organization_card, timeout=LONG)
        logger.info("[LoginPage]  Organisation selection screen is visible")

    def verify_org_selected(self) -> None:
        self.verify_visible(self.organization_card, timeout=DEFAULT)
        logger.info("[LoginPage]  Organisation 'Objectways' selected and visible")

    def verify_role_selected(self) -> None:
        self.verify_visible(self.company_admin_role, timeout=DEFAULT)
        logger.info("[LoginPage]  Role 'Company Admin' selected and visible")

    def verify_login_successful(self) -> None:
        expect(self.page).to_have_url(
            re.compile(r"tensoract\.com/$"), timeout=SHORT
        )
        logger.info("[LoginPage]  URL confirmed: dashboard root")
        self.verify_visible(self.welcome_heading, timeout=LONG)
        logger.info("[LoginPage]  'Welcome to Tensoract' heading visible")
        self.verify_visible(self.home_sidebar_link, timeout=DEFAULT)
        logger.info("[LoginPage]  Sidebar 'Home' link visible")
        logger.info("[LoginPage]  Login verified — admin is on dashboard")

    def verify_login_failed(self, expected_error: str = None) -> None:
        self.verify_url("/login")
        logger.info("[LoginPage]  Still on login page after failed attempt")
        if expected_error:
            error_locator = self.page.get_by_text(expected_error, exact=False)
            self.verify_visible(error_locator, timeout=DEFAULT)
            logger.info(f"[LoginPage]  Error message visible: '{expected_error}'")