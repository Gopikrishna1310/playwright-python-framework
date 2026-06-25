import logging
import pytest

from pages.common.login_page import LoginPage
from pages.users.users_page import UsersPage
from config.credentials import TOOL_EMAIL, TOOL_PASSWORD

logger = logging.getLogger(__name__)


@pytest.mark.users
def test_users_regression(page):

    # =========================================================================
    # LOGIN
    # =========================================================================

    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(TOOL_EMAIL, TOOL_PASSWORD)

    # =========================================================================
    # TC_07_01: Open Users page
    # =========================================================================

    users = UsersPage(page)

    # When: Click Users from sidebar
    users.open_users_page()

    # Then: Users list page should open
    users.verify_users_page_opened()
    logger.info("TC_07_01 Users page opened and verified")

    # =========================================================================
    # TC_07_02: Create User 1
    # =========================================================================

    # When: Click Create User button
    # Then: Create User popup should open (verified inside create_user())
    users.create_user(
        full_name="User 1",
        email="user1@objectways.com",
        password="User123!",
        roles=["Annotator"]
    )

    # Then: Create User popup should be closed after successful creation
    users.verify_create_user_popup_closed()

    # Then: New user should be added to the list
    users.verify_user_in_list("user1@objectways.com")
    logger.info("TC_07_02 User 1 created and verified in list")

    # =========================================================================
    # TC_07_02: Create User 2
    # =========================================================================

    users.create_user(
        full_name="User 2",
        email="user2@objectways.com",
        password="User123!",
        roles=["Annotator", "Reviewer"]
    )

    users.verify_create_user_popup_closed()
    users.verify_user_in_list("user2@objectways.com")
    logger.info("TC_07_02 User 2 created and verified in list")

    # =========================================================================
    # TC_07_03: Single user status change — Deactivate User 2
    # =========================================================================

    # Then: Change Status button should be disabled by default
    users.verify_change_status_disabled()

    # When: Select user2 checkbox
    users._user_row("user2@objectways.com").get_by_role("checkbox").check()

    # Then: Change Status button should be enabled
    users.verify_change_status_enabled()

    # When: Click Change Status
    users.safe_click(users.change_status_btn)

    # Then: Deactivate option should be visible (user is Active)
    users.verify_status_option_visible("Deactivate")

    # When: Click Deactivate
    users.safe_click(page.get_by_role("button", name="Deactivate"))

    users._reload_users_page()

    # Then: User should now be Inactive
    users.verify_user_status("user2@objectways.com", "Inactive")

    # Then: User should still appear in the list
    users.verify_user_still_in_list("user2@objectways.com")
    logger.info("TC_07_03 User 2 deactivated and verified Inactive — still in list")

    # =========================================================================
    # TC_07_03: Single user status change — Deactivate User 1
    # =========================================================================

    users.change_single_user_status(
        user_identifier="user1@objectways.com",
        action="Deactivate",
        expected_status="Inactive"
    )

    users.verify_user_still_in_list("user1@objectways.com")
    logger.info("TC_07_03 User 1 deactivated and verified Inactive — still in list")

    # =========================================================================
    # TC_07_04: Bulk status change — Activate user2 + reviewer
    # =========================================================================

    # When: Select two users (one Inactive, one Active)
    users._user_row("user2@objectways.com").get_by_role("checkbox").check()
    users._user_row("reviewer@objectways.com").get_by_role("checkbox").check()

    # Then: Change Status button should be enabled
    users.verify_change_status_enabled()

    # When: Click Change Status
    users.safe_click(users.change_status_btn)

    # Then: Both Activate and Deactivate options should be visible
    users.verify_both_status_options_visible()

    # When: Click Activate
    users.safe_click(page.get_by_role("button", name="Activate", exact=True).nth(0))

    users._reload_users_page()

    # Then: Both users should now be Active
    users.verify_user_status("user2@objectways.com", "Active")
    users.verify_user_status("reviewer@objectways.com", "Active")
    logger.info("TC_07_04 Bulk activate verified — both users Active")

    logger.info("Users regression completed successfully")