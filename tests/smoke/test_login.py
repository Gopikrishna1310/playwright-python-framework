import pytest
import logging

from pages.common.login_page import LoginPage
from config.credentials import ADMIN_EMAIL, ADMIN_PASSWORD

logger = logging.getLogger(__name__)


# =============================================================================
# TC_01_01 + TC_01_02: Login Flow
# =============================================================================
#
# Scenario:
#   1. Attempt login with invalid credentials  (negative case)
#   2. Clear fields and login with valid credentials  (positive case)
#
# Both run in the same browser session — no re-navigation needed.
#
# =============================================================================

@pytest.mark.smoke
def test_login(page):

    login_page = LoginPage(page)

    # Given: I am on the login page
    login_page.open_login_page()

    # =========================================================================
    # TC_01_02: Invalid login (negative case — runs first)
    # =========================================================================

    # When: Enter invalid credentials and click Sign In
    login_page.enter_credentials("invalid@email.com", "WrongPassword123!")

    # Then: User should remain on login page with an error message
    login_page.verify_login_failed(expected_error="not found")
    logger.info("TC_01_02 Step verified: Login rejected, error message shown")
    logger.info("TC_01_02 Invalid login — PASSED")

    # =========================================================================
    # TC_01_01: Valid login (positive case — runs after negative)
    # =========================================================================

    # When: Clear fields and enter valid credentials
    login_page.clear_credentials()
    login_page.enter_credentials(ADMIN_EMAIL, ADMIN_PASSWORD)

    # Then: Organisation selection screen should be displayed
    login_page.verify_org_selection_visible()
    logger.info("TC_01_01 Step verified: Organisation selection screen displayed")

    # When: Select organisation
    login_page.select_organization()

    # Then: Organisation should be selected
    login_page.verify_org_selected()
    logger.info("TC_01_01 Step verified: Organisation selected")

    # When: Select Company Admin role
    login_page.select_role()

    # Then: Company Admin role should be selected
    login_page.verify_role_selected()
    logger.info("TC_01_01 Step verified: Role 'Company Admin' selected")

    # When: Click Continue
    login_page.click_continue()

    # Then: Admin home page should be displayed
    login_page.verify_login_successful()
    logger.info("TC_01_01 Step verified: Admin home page displayed")
    logger.info("TC_01_01 Valid login as Company Admin — PASSED")