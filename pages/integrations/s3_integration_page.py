from playwright.sync_api import (
    Page
)

from pages.common.base_page import (
    BasePage
)


class S3IntegrationPage(BasePage):

    def __init__(self, page: Page):

        super().__init__(page)

        self.new_integration_button = page.get_by_role(
            "button",
            name="New Integration"
        )

        self.step1_dropdown = page.get_by_text(
            "Give Your integration a title"
        )

    # ============================================
    # OPEN NEW INTEGRATION POPUP
    # ============================================

    def open_new_integration_popup(self):

        self.safe_click(
            self.new_integration_button
        )

        self.safe_click(
            self.step1_dropdown
        )

    # ============================================
    # ENTER BASIC DETAILS
    # ============================================

    def enter_basic_details(
        self,
        integration_title,
        bucket_name
    ):

        title_input = self.page.get_by_placeholder(
            "Integration title"
        )

        self.safe_fill(
            title_input,
            integration_title
        )

        bucket_input = self.page.get_by_placeholder(
            "S3 bucket name"
        )

        self.safe_fill(
            bucket_input,
            bucket_name
        )

        self.page.wait_for_timeout(1000)

    # ============================================
    # OPEN STEP 2
    # ============================================

    def open_step_2(self):

        step2_dropdown = self.page.get_by_text(
            "Create an IAM permission"
        )

        self.safe_click(
            step2_dropdown
        )

        self.page.wait_for_timeout(1000)

    # ============================================
    # GET POLICY JSON
    # ============================================

    def get_policy_json(self):

        copy_button = self.page.get_by_role(
            "button",
            name="Copy"
        ).first

        self.safe_click(
            copy_button
        )

        # Clipboard stabilization wait
        self.page.wait_for_timeout(1500)

        policy_json = self.page.evaluate(
            "navigator.clipboard.readText()"
        )

        return policy_json

    # ============================================
    # OPEN STEP 3
    # ============================================

    def open_step_3(self):

        step3_dropdown = self.page.get_by_text(
            "Create an IAM role"
        )

        self.safe_click(
            step3_dropdown
        )

        self.page.wait_for_timeout(1000)

    # ============================================
    # GET ACCOUNT ID
    # ============================================

    def get_account_id(self):

        copy_button = self.page.get_by_role(
            "button",
            name="Copy"
        ).nth(1)

        self.safe_click(
            copy_button
        )

        # Clipboard stabilization wait
        self.page.wait_for_timeout(1500)

        account_id = self.page.evaluate(
            "navigator.clipboard.readText()"
        )

        return account_id

    # ============================================
    # GET EXTERNAL ID
    # ============================================

    def get_external_id(self):

        copy_button = self.page.get_by_role(
            "button",
            name="Copy"
        ).nth(2)

        self.safe_click(
            copy_button
        )

        # Clipboard stabilization wait
        self.page.wait_for_timeout(1500)

        external_id = self.page.evaluate(
            "navigator.clipboard.readText()"
        )

        return external_id

    # ============================================
    # PASTE ROLE ARN
    # ============================================

    def paste_role_arn(self):

        role_arn_input = self.page.get_by_placeholder(
            "Role ARN"
        )

        role_arn_input.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            role_arn_input
        )

        self.page.keyboard.press(
            "Control+V"
        )

        self.page.wait_for_timeout(1500)

        print("\nRole ARN pasted")

    # ============================================
    # OPEN STEP 4
    # ============================================

    def open_step_4(self):

        step4_dropdown = self.page.get_by_text(
            "Set CORS permissions"
        )

        step4_dropdown.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            step4_dropdown
        )

        self.page.wait_for_timeout(1000)

        print("\nStep 4 opened")

    # ============================================
    # COPY CORS JSON
    # ============================================

    def copy_cors_json(self):

        copy_button = self.page.get_by_role(
            "button",
            name="Copy"
        ).nth(3)

        copy_button.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            copy_button
        )

        # Clipboard stabilization wait
        self.page.wait_for_timeout(1500)

        cors_json = self.page.evaluate(
            "navigator.clipboard.readText()"
        )

        print("\nCORS JSON copied")

        return cors_json

    # ============================================
    # CLICK CREATE INTEGRATION
    # ============================================

    def click_create_integration(self):

        create_button = self.page.get_by_role(
            "button",
            name="Create",
            exact=True
        )

        create_button.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            create_button
        )

        self.page.wait_for_timeout(3000)

        print("\nCreate Integration clicked")

    # ============================================
    # VALIDATE INTEGRATION CREATED
    # ============================================

    def validate_integration_created(self):

        self.page.wait_for_url(
            "**/s3-connections",
            timeout=60000
        )

        current_url = self.page.url

        assert "s3-connections" in current_url

        print(
            "\nIntegration validation completed"
        )

    # ============================================
    # CLICK RUN A TEST
    # ============================================

    def click_run_a_test(self):

        run_test_button = self.page.get_by_role(
            "button",
            name="Run a test"
        ).first

        run_test_button.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            run_test_button
        )

        self.page.wait_for_timeout(2000)

        print("\nRun a Test popup opened")

    # ============================================
    # ENTER S3 URL
    # ============================================

    def enter_s3_url(
        self,
        s3_url
    ):

        s3_input = self.page.get_by_role(
            "textbox",
            name="* Enter object URL to test"
        )

        s3_input.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_fill(
            s3_input,
            s3_url
        )

        self.page.wait_for_timeout(1000)

        print("\nS3 URL entered")

    # ============================================
    # CLICK CHECK BUTTON
    # ============================================

    def click_check_button(self):

        check_button = self.page.get_by_role(
            "button",
            name="Check Field Mountain can"
        )

        check_button.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            check_button
        )

        self.page.wait_for_timeout(5000)

        print("\nCheck button clicked")

    # ============================================
    # VALIDATE TEST SUCCESS
    # ============================================

    def validate_test_success(self):

        self.page.wait_for_timeout(3000)

        print("\nIntegration test completed")