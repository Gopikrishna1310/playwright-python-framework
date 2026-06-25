from playwright.sync_api import Page

from pages.common.base_page import BasePage
from utils.waits import LONG, LOAD


class AWSLoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.account_input = page.get_by_role("textbox", name="Account ID or alias")
        self.username_input = page.get_by_role("textbox", name="IAM username")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.sign_in_button = page.get_by_test_id("sign-in")

    # =========================================================================
    # OPEN AWS LOGIN PAGE
    # =========================================================================

    def open_aws_login_page(self):
        self.page.goto(
            "https://eu-north-1.signin.aws.amazon.com/",
            wait_until="domcontentloaded",
            timeout=LOAD,
        )
        self.verify_visible(self.account_input, timeout=LOAD)

    # =========================================================================
    # LOGIN TO AWS
    # =========================================================================

    def login_to_aws(self, account_id, username, password):
        self.safe_fill(self.account_input, account_id)
        self.safe_fill(self.username_input, username)
        self.safe_fill(self.password_input, password)
        self.safe_click(self.sign_in_button)
        self.wait.for_hidden(self.sign_in_button, timeout=LONG)
        print("\nAWS login navigation complete")