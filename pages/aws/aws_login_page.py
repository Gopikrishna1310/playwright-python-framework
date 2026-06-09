from playwright.sync_api import (
    Page
)

from pages.common.base_page import (
    BasePage
)


class AWSLoginPage(BasePage):

    def __init__(self, page: Page):

        super().__init__(page)

    # ============================================
    # OPEN AWS LOGIN PAGE
    # ============================================

    def open_aws_login_page(self):

        self.page.goto(
            "https://eu-north-1.signin.aws.amazon.com/"
        )

        self.page.wait_for_load_state()

        # Wait for Account ID field
        self.page.get_by_role(
            "textbox",
            name="Account ID or alias"
        ).wait_for(
            state="visible",
            timeout=60000
        )

    # ============================================
    # LOGIN TO AWS
    # ============================================

    def login_to_aws(
        self,
        account_id,
        username,
        password
    ):

        # ========================================
        # ACCOUNT ID / ALIAS
        # ========================================

        account_input = self.page.get_by_role(
            "textbox",
            name="Account ID or alias"
        )

        self.safe_fill(
            account_input,
            account_id
        )

        # ========================================
        # IAM USERNAME
        # ========================================

        username_input = self.page.get_by_role(
            "textbox",
            name="IAM username"
        )

        self.safe_fill(
            username_input,
            username
        )

        # ========================================
        # PASSWORD
        # ========================================

        password_input = self.page.get_by_role(
            "textbox",
            name="Password"
        )

        self.safe_fill(
            password_input,
            password
        )

        # ========================================
        # SIGN IN
        # ========================================

        sign_in_button = self.page.get_by_test_id(
            "sign-in"
        )

        self.safe_click(
            sign_in_button
        )

        # ========================================
        # WAIT FOR AWS CONSOLE LOAD
        # ========================================

        self.page.wait_for_load_state()

        # AWS redirect stabilization
        self.page.wait_for_timeout(3000)