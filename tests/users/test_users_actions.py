import pytest

from pages.common.login_page import LoginPage

from pages.users.users_page import UsersPage

from config.credentials import (
    TOOL_EMAIL,
    TOOL_PASSWORD
)


@pytest.mark.users
def test_users_regression(page):

    # ============================================
    # LOGIN
    # ============================================

    login_page = LoginPage(page)

    login_page.open_login_page()

    login_page.login(
        TOOL_EMAIL,
        TOOL_PASSWORD
    )

    print(
        "\nLogin successful"
    )

    # ============================================
    # USERS PAGE
    # ============================================

    users = UsersPage(page)

    users.open_users_page()

    # ============================================
    # TC_07_02 - CREATE USER 1
    # ============================================

    users.create_user(
        full_name="User 1",
        email="user1@objectways.com",
        password="User123!",
        roles=["Annotator"]
    )

    print(
        "\nUser 1 created successfully"
    )

    # ============================================
    # TC_07_02 - CREATE USER 2
    # ============================================

    users.create_user(
        full_name="User 2",
        email="user2@objectways.com",
        password="User123!",
        roles=[
            "Annotator",
            "Reviewer"
        ]
    )

    print(
        "\nUser 2 created successfully"
    )

    # ============================================
    # TC_07_03 - SINGLE USER STATUS CHANGE
    # ============================================

    users.change_single_user_status(
        user_identifier="user2@objectways.com",
        action="Deactivate",
        expected_status="Inactive"
    )

    print(
        "\nSingle user status changed successfully"
    )

    # ============================================
    # TC_07_03 - SECOND USER STATUS CHANGE
    # ============================================

    users.change_single_user_status(
        user_identifier="user1@objectways.com",
        action="Deactivate",
        expected_status="Inactive"
    )

    print(
        "\nSecond user status changed successfully"
    )

    # ============================================
    # TC_07_04 - BULK STATUS CHANGE
    # ============================================

    users.bulk_change_status(
        user_identifiers=[
            "user2@objectways.com",
            "reviewer@"
        ],
        action="Activate",
        expected_status="Active"
    )

    print(
        "\nBulk user status change completed successfully"
    )

    # ============================================
    # FINAL MESSAGE
    # ============================================

    print(
        "\nUsers regression completed successfully"
    )