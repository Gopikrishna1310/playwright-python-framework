import re

from playwright.sync_api import (
    expect,
    Page
)

from pages.common.base_page import BasePage


class UsersPage(BasePage):

    def __init__(
            self,
            page: Page
    ):

        super().__init__(page)

        self.users_menu = page.get_by_role(
            "link",
            name="Users"
        )

    # ============================================
    # OPEN USERS PAGE
    # ============================================

    def open_users_page(self):

        self.safe_click(
            self.users_menu
        )

        self.page.wait_for_timeout(2000)

        expect(
            self.page.get_by_role(
                "heading",
                name="Users"
            )
        ).to_be_visible()

        print(
            "\nUsers page opened"
        )

    # ============================================
    # CREATE USER
    # ============================================

    def create_user(
            self,
            full_name,
            email,
            password,
            roles
    ):

        create_user_button = self.page.get_by_role(
            "button",
            name="Create User"
        )

        self.safe_click(
            create_user_button
        )

        expect(
            self.page.get_by_role(
                "heading",
                name="Create User"
            )
        ).to_be_visible()

        print(
            "\nCreate User popup opened"
        )

        self.page.wait_for_timeout(1000)

        # ============================================
        # FILL USER DETAILS
        # ============================================

        self.safe_fill(
            self.page.get_by_role(
                "textbox",
                name="Enter Full Name"
            ),
            full_name
        )

        self.safe_fill(
            self.page.get_by_role(
                "textbox",
                name="Enter Email"
            ),
            email
        )

        self.safe_fill(
            self.page.get_by_role(
                "textbox",
                name="Enter Password"
            ),
            password
        )

        self.safe_fill(
            self.page.get_by_role(
                "textbox",
                name="Confirm Password"
            ),
            password
        )

        print(
            f"\nFilled user details for: {full_name}"
        )

        # ============================================
        # OPEN ROLES DROPDOWN
        # ============================================

        roles_dropdown = self.page.get_by_role(
            "button",
            name="Select roles"
        )

        self.safe_click(
            roles_dropdown
        )

        print(
            "\nRoles dropdown opened"
        )

        self.page.wait_for_timeout(1000)

        # ============================================
        # SELECT ROLES
        # ============================================

        for role in roles:

            role_option = (
                self.page
                .locator("div")
                .filter(
                    has_text=re.compile(
                        rf"^{role}$"
                    )
                )
            )

            self.safe_click(
                role_option
            )

            print(
                f"\nSelected role: {role}"
            )

            self.page.wait_for_timeout(500)

        # ============================================
        # CLOSE ROLES DROPDOWN
        # ============================================

        self.page.mouse.click(
            50,
            50
        )

        self.page.wait_for_timeout(1000)

        print(
            "\nRoles dropdown closed"
        )

        # ============================================
        # CREATE USER
        # ============================================

        create_button = (
            self.page
            .get_by_role(
                "button",
                name="Create User"
            )
            .last
        )

        self.safe_click(
            create_button
        )

        print(
            f"\nClicked Create User for: {full_name}"
        )

        # Backend propagation stabilization

        self.page.wait_for_timeout(3000)

        # ============================================
        # VERIFY TOAST
        # ============================================

        expect(
            self.page.get_by_text(
                "User created"
            )
        ).to_be_visible()

        print(
            "\nUser creation toast verified"
        )

        # ============================================
        # VERIFY USER ADDED
        # ============================================

        expect(
            self.page.get_by_role(
                "row",
                name=re.compile(email)
            )
        ).to_be_visible()

        print(
            f"\nVerified user added:\n{email}"
        )

    # ============================================
    # CHANGE SINGLE USER STATUS
    # ============================================

    def change_single_user_status(
            self,
            user_identifier,
            action,
            expected_status
    ):

        change_status_button = self.page.get_by_role(
            "button",
            name="Change Status"
        )

        expect(
            change_status_button
        ).to_be_disabled()

        print(
            "\nChange Status button initially disabled"
        )

        # ============================================
        # SELECT USER
        # ============================================

        user_row = self.page.get_by_role(
            "row",
            name=re.compile(user_identifier)
        )

        user_row.get_by_role(
            "checkbox"
        ).check()

        print(
            f"\nSelected user:\n{user_identifier}"
        )

        self.page.wait_for_timeout(1000)

        expect(
            change_status_button
        ).to_be_enabled()

        print(
            "\nChange Status button enabled"
        )

        # ============================================
        # OPEN STATUS MENU
        # ============================================

        self.safe_click(
            change_status_button
        )

        self.page.wait_for_timeout(1000)

        # ============================================
        # CLICK ACTION
        # ============================================

        action_button = self.page.get_by_role(
            "button",
            name=action
        )

        expect(
            action_button
        ).to_be_visible()

        self.safe_click(
            action_button
        )

        print(
            f"\nStatus changed to:\n{action}"
        )

        # Backend propagation stabilization

        self.page.wait_for_timeout(3000)

        # ============================================
        # VERIFY UPDATED STATUS
        # ============================================

        expect(
            self.page.get_by_role(
                "row",
                name=re.compile(user_identifier)
            ).get_by_text(
                expected_status
            )
        ).to_be_visible()

        print(
            f"\nVerified updated status:\n{expected_status}"
        )

    # ============================================
    # BULK CHANGE STATUS
    # ============================================

    def bulk_change_status(
            self,
            user_identifiers,
            action,
            expected_status
    ):

        change_status_button = self.page.get_by_role(
            "button",
            name="Change Status"
        )

        expect(
            change_status_button
        ).to_be_disabled()

        print(
            "\nChange Status button initially disabled"
        )

        # ============================================
        # SELECT USERS
        # ============================================

        for user in user_identifiers:

            user_row = self.page.get_by_role(
                "row",
                name=re.compile(user)
            )

            user_row.get_by_role(
                "checkbox"
            ).check()

            print(
                f"\nSelected user:\n{user}"
            )

            self.page.wait_for_timeout(500)

        expect(
            change_status_button
        ).to_be_enabled()

        print(
            "\nChange Status button enabled"
        )

        # ============================================
        # OPEN STATUS MENU
        # ============================================

        self.safe_click(
            change_status_button
        )

        self.page.wait_for_timeout(1000)

        # ============================================
        # VERIFY OPTIONS
        # ============================================

        expect(
            self.page.get_by_role(
                "button",
                name="Activate",
                exact=True
            ).nth(0)
        ).to_be_visible()

        expect(
            self.page.get_by_role(
                "button",
                name="Deactivate",
                exact=True
            ).nth(0)
        ).to_be_visible()

        print(
            "\nActivate and Deactivate options verified"
        )

        # ============================================
        # CLICK ACTION
        # ============================================

        action_button = (
            self.page
            .get_by_role(
                "button",
                name=action,
                exact=True
            )
            .nth(0)
        )

        self.safe_click(
            action_button
        )

        print(
            f"\nBulk status changed to:\n{action}"
        )

        # Backend propagation stabilization

        self.page.wait_for_timeout(3000)

        # ============================================
        # VERIFY UPDATED STATUS
        # ============================================

        for user in user_identifiers:

            expect(
                self.page.get_by_role(
                    "row",
                    name=re.compile(user)
                ).get_by_text(
                    expected_status
                )
            ).to_be_visible()

            print(
                f"\nVerified updated status for {user}: {expected_status}"
            )