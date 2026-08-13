import re
from utils.ui_utils import UIUtils

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.email_input       = page.get_by_role("textbox", name="Email")
        self.password_input    = page.get_by_role("textbox", name="Password")
        self.sign_in_button    = page.get_by_role("button",  name="Sign in", exact=True)
        self.sign_In_button    = page.get_by_role("button",  name="Sign In", exact=True)
        self.organization_card = page.get_by_role("heading", name="Test Company B")
        self.company_admin_role = page.get_by_role("paragraph").filter(has_text=re.compile(r"^Company Admin$"))
        self.continue_button   = page.get_by_role("button", name="Continue")
        self.welcome_heading   = page.get_by_role("heading", name="Welcome to Tensoract")
        self.home_sidebar_link = page.get_by_role("link", name="Home")
        self.back_to_login = page.locator("button:has-text('Back to Login')")
        self.home_icon = page.get_by_text("Home")
        self.home_page_welcome = page.get_by_role('heading', name = 'Welcome to Tensoract' )
        self.different_email_for_otp_link = page.get_by_role('button', name = 'Send code to a different email' )
        self.email_address_input = page.get_by_role('textbox', name = 'Email Address' )
        self.send_code_button = page.get_by_role('button', name = 'Send Code' )
        self.enter_otp_input = page.locator("div").filter(has_text=re.compile(r"^Enter OTP$"))

    def get_organization_option(self, organization_name):
        return self.page.get_by_text(organization_name, exact=True)

    def enter_otp(self, index):
        return self.page.locator(f'#otp-digit-{index}')