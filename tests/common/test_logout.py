import pytest

from pages.common.login_page import LoginPage
from pages.common.sidebar_page import SidebarPage
from pages.common.logout_page import LogoutPage

from config.credentials import (
    TOOL_EMAIL,
    TOOL_PASSWORD
)


@pytest.mark.common
def test_logout(page):

    # ============================================
    # LOGIN
    # ============================================

    login_page = LoginPage(page)

    login_page.open_login_page()

    login_page.login(
        TOOL_EMAIL,
        TOOL_PASSWORD
    )

    # ============================================
    # ORGANIZATION + ROLE
    # ============================================

    sidebar_page = SidebarPage(page)

    sidebar_page.select_organization_and_role()

    print(
        "\nLogin successful"
    )

    # ============================================
    # LOGOUT PAGE
    # ============================================

    logout_page = LogoutPage(page)

    # ============================================
    # TC_10_01
    # LOGOUT FLOW
    # ============================================

    logout_page.open_profile_menu()

    logout_page.validate_profile_options()

    logout_page.logout()

    logout_page.validate_logout_successful()

    print(
        "\nTC_10_01 Logout validation completed"
    )