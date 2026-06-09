from playwright.sync_api import (
    Page
)

from pages.common.base_page import (
    BasePage
)


class LoginPage(BasePage):

    def __init__(self, page: Page):

        super().__init__(page)

        # ============================================
        # LOGIN ELEMENTS
        # ============================================

        self.email_input = page.get_by_role(
            "textbox",
            name="Email"
        )

        self.password_input = page.get_by_role(
            "textbox",
            name="Password"
        )

        self.sign_in_button = page.get_by_role(
            "button",
            name="Sign in"
        )

    # ============================================
    # OPEN LOGIN PAGE
    # ============================================

    def open_login_page(self):

        self.open_url(
            "https://fmn-qa.tensoract.com/login"
        )

    # ============================================
    # LOGIN
    # ============================================

    def login(
        self,
        username,
        password
    ):

        # ========================================
        # ENTER EMAIL
        # ========================================

        self.safe_fill(
            self.email_input,
            username
        )

        # ========================================
        # ENTER PASSWORD
        # ========================================

        self.safe_fill(
            self.password_input,
            password
        )

        # ========================================
        # CLICK SIGN IN
        # ========================================

        self.safe_click(
            self.sign_in_button
        )

        # ========================================
        # WAIT AFTER SIGN IN
        # ========================================

        self.page.wait_for_load_state()

        self.page.wait_for_timeout(3000)

        # ========================================
        # HANDLE ORGANIZATION + ROLE SCREEN
        # ========================================

        try:

            # ====================================
            # SELECT ORGANIZATION
            # ====================================

            organization_card = self.page.get_by_text(
                "Objectways"
            )

            organization_card.wait_for(
                state="visible",
                timeout=15000
            )

            self.safe_click(
                organization_card
            )

            # ====================================
            # SELECT ROLE
            # ====================================

            company_admin_role = self.page.get_by_text(
                "Company Admin",
                exact=True
            )

            company_admin_role.wait_for(
                state="visible",
                timeout=10000
            )

            self.safe_click(
                company_admin_role
            )

            # ====================================
            # CLICK CONTINUE
            # ====================================

            continue_button = self.page.get_by_role(
                "button",
                name="Continue"
            )

            self.safe_click(
                continue_button
            )

            # ====================================
            # WAIT FOR SUCCESSFUL REDIRECTION
            # ====================================

            self.page.wait_for_url(
                "https://fmn-qa.tensoract.com/",
                timeout=60000
            )

            print(
                "\nOrganization and role selected"
            )

        except Exception as e:

            print(
                f"\nOrganization handling skipped: {e}"
            )

        # ========================================
        # FINAL STABILIZATION WAIT
        # ========================================

        self.page.wait_for_timeout(2000)