from playwright.sync_api import (
    Page
)

from pages.common.base_page import (
    BasePage
)


class AWSRolePage(BasePage):

    def __init__(self, page: Page):

        super().__init__(page)

    # ============================================
    # OPEN ROLES PAGE
    # ============================================

    def open_roles_page(self):

        self.page.goto(
            "https://us-east-1.console.aws.amazon.com/iam/home#/roles"
        )

        self.page.wait_for_load_state()

        self.page.wait_for_url(
            "**/roles",
            timeout=60000
        )

        print("\nRoles page opened")

    # ============================================
    # CLICK CREATE ROLE
    # ============================================

    def click_create_role(self):

        create_role_button = self.page.get_by_role(
            "button",
            name="Create role"
        )

        create_role_button.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            create_role_button
        )

        # AWS form stabilization
        self.page.wait_for_timeout(2000)

        print("\nCreate Role page opened")

    # ============================================
    # SELECT AWS ACCOUNT
    # ============================================

    def select_aws_account(self):

        aws_account_option = self.page.get_by_text(
            "AWS account",
            exact=True
        )

        self.safe_click(
            aws_account_option.first
        )

        self.page.wait_for_timeout(1500)

        print("\nAWS Account selected")

    # ============================================
    # SELECT ANOTHER AWS ACCOUNT
    # ============================================

    def select_another_aws_account(self):

        another_account = self.page.get_by_text(
            "Another AWS account",
            exact=True
        )

        self.safe_click(
            another_account.first
        )

        self.page.wait_for_timeout(1500)

        print("\nAnother AWS Account selected")

    # ============================================
    # ENTER ACCOUNT ID
    # ============================================

    def enter_account_id(
        self,
        account_id
    ):

        account_input = self.page.get_by_role(
            "textbox",
            name="Account ID"
        )

        account_input.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_fill(
            account_input,
            account_id
        )

        self.page.wait_for_timeout(1500)

        print("\nAccount ID entered")

    # ============================================
    # ENABLE EXTERNAL ID
    # ============================================

    def enable_external_id(self):

        external_id_checkbox = self.page.get_by_role(
            "checkbox",
            name="Require external ID"
        )

        external_id_checkbox.check()

        self.page.wait_for_timeout(1500)

        print("\nExternal ID enabled")

    # ============================================
    # ENTER EXTERNAL ID
    # ============================================

    def enter_external_id(
        self,
        external_id
    ):

        external_id_input = self.page.get_by_role(
            "textbox",
            name="External ID"
        )

        external_id_input.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_fill(
            external_id_input,
            external_id
        )

        self.page.wait_for_timeout(1500)

        print("\nExternal ID entered")

    # ============================================
    # GO TO PERMISSIONS PAGE
    # ============================================

    def go_to_permissions_page(self):

        next_button = self.page.get_by_role(
            "button",
            name="Next"
        ).last

        next_button.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            next_button
        )

        # AWS permissions page rendering
        self.page.wait_for_timeout(3000)

        print("\nMoved to permissions page")

    # ============================================
    # ATTACH POLICY
    # ============================================

    def attach_policy(
        self,
        policy_name
    ):

        search_input = self.page.get_by_role(
            "searchbox"
        )

        search_input.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_fill(
            search_input,
            policy_name
        )

        # AWS table refresh
        self.page.wait_for_timeout(3000)

        print("\nPolicy searched")

        policy_checkbox = self.page.get_by_role(
            "checkbox",
            name=policy_name
        )

        policy_checkbox.wait_for(
            state="visible",
            timeout=60000
        )

        policy_checkbox.check()

        self.page.wait_for_timeout(1500)

        print("\nPolicy selected")

        next_button = self.page.get_by_role(
            "button",
            name="Next",
            exact=True
        )

        self.safe_click(
            next_button
        )

        # Review page stabilization
        self.page.wait_for_timeout(3000)

        print("\nMoved to review page")

    # ============================================
    # ENTER ROLE NAME
    # ============================================

    def enter_role_name(
        self,
        role_name
    ):

        role_name_input = self.page.get_by_role(
            "textbox",
            name="Role name"
        )

        role_name_input.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_fill(
            role_name_input,
            role_name
        )

        self.page.wait_for_timeout(1500)

        print("\nRole name entered")

    # ============================================
    # CREATE ROLE
    # ============================================

    def create_role(self):

        create_role_button = self.page.get_by_role(
            "button",
            name="Create role",
            exact=True
        )

        create_role_button.wait_for(
            state="visible",
            timeout=60000
        )

        # Scroll to bottom
        self.page.mouse.wheel(
            0,
            3000
        )

        self.page.wait_for_timeout(1000)

        # First click
        self.safe_click(
            create_role_button
        )

        print("\nFirst Create Role click done")

        # AWS processing stabilization
        self.page.wait_for_timeout(3000)

        # Second click if still present
        try:

            create_role_button.click(
                force=True,
                timeout=5000
            )

            print("\nSecond Create Role click done")

        except:

            print(
                "\nRole creation page already changed"
            )

        # Final AWS redirect stabilization
        self.page.wait_for_load_state()

        self.page.wait_for_timeout(5000)

        print("\nCreate role process completed")

    # ============================================
    # OPEN CREATED ROLE
    # ============================================

    def open_created_role(
        self,
        role_name
    ):

        view_role_button = self.page.get_by_role(
            "button",
            name=f"View role {role_name}"
        )

        view_role_button.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            view_role_button
        )

        self.page.wait_for_timeout(3000)

        print("\nOpened created role")

    # ============================================
    # COPY ROLE ARN
    # ============================================

    def copy_role_arn(self):

        copy_arn_button = self.page.get_by_role(
            "button",
            name="Copy ARN"
        )

        copy_arn_button.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            copy_arn_button
        )

        # Clipboard stabilization
        self.page.wait_for_timeout(1500)

        print("\nRole ARN copied")