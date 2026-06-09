from playwright.sync_api import (
    expect
)


class LogoutPage:

    def __init__(self, page):

        self.page = page

    # ============================================
    # OPEN PROFILE MENU
    # ============================================

    def open_profile_menu(self):

        self.page.locator(
            "span.font-medium.text-\\[\\#312E81\\]"
        ).click()

        print(
            "\nProfile menu opened"
        )

    # ============================================
    # VALIDATE MENU OPTIONS
    # ============================================

    def validate_profile_options(self):

        expect(
            self.page.get_by_text(
                "SWITCH ROLE"
            )
        ).to_be_visible()

        expect(
            self.page.get_by_role(
                "button",
                name="Logout"
            )
        ).to_be_visible()

        print(
            "\nSwitch Roles and Logout options validated"
        )

    # ============================================
    # LOGOUT
    # ============================================

    def logout(self):

        self.page.get_by_role(
            "button",
            name="Logout"
        ).click()

        print(
            "\nLogout button clicked"
        )

    # ============================================
    # VALIDATE LOGIN PAGE
    # ============================================

    def validate_logout_successful(self):

        expect(
            self.page.get_by_role(
                "button",
                name="Sign in"
            )
        ).to_be_visible()

        print(
            "\nLogout successful"
        )