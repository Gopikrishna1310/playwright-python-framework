import re
import time

from playwright.sync_api import Page, expect

from pages.common.base_page import BasePage
from utils.waits import SHORT, DEFAULT, LONG, LOAD


class S3IntegrationPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.new_integration_button = page.get_by_role("button", name="New Integration")
        self.popup_heading           = page.get_by_role("heading", name="Add S3 Integration")
        self.step1_dropdown          = page.get_by_text("Give Your integration a title")
        self.step2_dropdown          = page.get_by_text("Create an IAM permission policy")
        self.step3_dropdown          = page.get_by_text("Create an IAM role")
        self.step4_dropdown          = page.get_by_text("Set CORS permissions")
        self.title_input             = page.get_by_placeholder("Integration title")
        self.bucket_input            = page.get_by_placeholder("S3 bucket name")
        self.role_arn_input          = page.get_by_placeholder("Role ARN")
        # Step 3 fields — DevTools confirmed exact selectors:
        #   Account ID:  <input readonly placeholder="AWS Account ID" ...>
        #   External ID: <input id="externalId" placeholder="External id" ...>
        # Each row's "Copy" button is scoped via has=, not global .nth()
        # indices, so it stays correct even if Step 2's policy-JSON Copy
        # button is added/removed/reordered.
        self.account_id_input        = page.get_by_placeholder("AWS Account ID")
        self.external_id_input       = page.locator("#externalId")

        # filter(has=...) matched 3 ancestor divs (too broad — caught both
        # Copy buttons via outer wrapper divs). xpath=".." steps to the
        # DIRECT parent only, which is the immediate flex-row sibling of
        # the input and its one Copy button — confirmed via DevTools as a
        # tight container, not a section wrapper.
        self.account_id_copy_button  = self.account_id_input.locator(
            "xpath=.."
        ).get_by_role("button", name="Copy")

        self.external_id_copy_button = self.external_id_input.locator(
            "xpath=.."
        ).get_by_role("button", name="Copy")
        self.create_button           = page.get_by_role("button", name="Create", exact=True)
        self.success_toast_heading   = page.get_by_text("Successfully created Integration")
        self.run_test_button         = page.get_by_role("button", name="Run a test").first
        self.test_popup_heading      = page.get_by_role("heading", name="Test Integration")
        self.test_url_input          = page.get_by_role("textbox", name="* Enter object URL to test")
        self.check_button            = page.get_by_role("button", name="Check Field Mountain can access this URL")

    # =========================================================================
    # ASSERTIONS
    # =========================================================================

    def verify_popup_opened(self) -> None:
        self.verify_visible(self.popup_heading, timeout=DEFAULT)
        print("\nAdd S3 Integration popup opened")

    def verify_policy_json_visible(self) -> None:
        policy_json_block = self.page.get_by_text('"Version": "2012-10-17"')
        self.verify_visible(policy_json_block, timeout=DEFAULT)
        print("\nPolicy JSON visible")

    def verify_account_external_id_fields_visible(self) -> None:
        self.verify_visible(self.account_id_input, timeout=DEFAULT)
        self.verify_visible(self.external_id_input, timeout=DEFAULT)
        print("\nAccount ID and External ID fields visible")

    def verify_cors_json_visible(self) -> None:
        cors_json_block = self.page.get_by_text('"AllowedHeaders"')
        self.verify_visible(cors_json_block, timeout=DEFAULT)
        print("\nCORS JSON visible")

    def verify_integration_created(self) -> None:
        # Toast notification is transient (auto-dismisses after a few
        # seconds) and the AWS round-trip before this point takes minutes,
        # so the toast is almost certainly gone by the time this runs.
        # Only the URL redirect is checked here — row visibility is its
        # own explicit step via verify_integration_visible_in_list(),
        # called separately before Run a Test.
        self.wait.for_url_contains("/s3-connections", timeout=LONG)
        assert "s3-connections" in self.page.url
        print("\nIntegration creation redirect confirmed")

    def verify_integration_visible_in_list(self, integration_title: str) -> None:
        """
        Explicit gate before Run a Test: confirms the integration row is
        visible in the list. Run a Test depends on this row existing, so
        this is checked as its own step rather than folded into creation.
        """
        row = self.page.get_by_role("row", name=integration_title)
        self.verify_visible(row.first, timeout=LONG)
        print(f"\nIntegration '{integration_title}' visible in list")

    def verify_test_popup_opened(self) -> None:
        self.verify_visible(self.test_popup_heading, timeout=DEFAULT)
        self.verify_visible(self.test_url_input, timeout=DEFAULT)
        print("\nTest Integration popup opened")

    def verify_test_success(self) -> None:
        file_msg = self.page.get_by_text(
            "The file is accessible from Field Mountain infrastructure"
        )
        machine_msg = self.page.get_by_text(
            "The content is accessible from this machine"
        )
        self.verify_visible(file_msg, timeout=LONG)
        print("\n Field Mountain infrastructure access confirmed")
        self.verify_visible(machine_msg, timeout=LONG)
        print(" Local machine access confirmed")
        print("\nIntegration test PASSED — both access checks succeeded")

    # =========================================================================
    # POPUP / STEP 1
    # =========================================================================

    def open_new_integration_popup(self) -> None:
        self.safe_click(self.new_integration_button)
        self.safe_click(self.step1_dropdown)

    def enter_basic_details(self, integration_title: str, bucket_name: str) -> None:
        self.safe_fill(self.title_input, integration_title)
        self.safe_fill(self.bucket_input, bucket_name)

    # =========================================================================
    # STEP 2 — IAM POLICY
    # =========================================================================

    def open_step_2(self) -> None:
        self.safe_click(self.step2_dropdown)

    def get_policy_json(self) -> str:
        self.safe_click(self.page.get_by_role("button", name="Copy").first)
        return self.read_clipboard(expected_prefix="{")

    # =========================================================================
    # STEP 3 — IAM ROLE
    # =========================================================================

    def open_step_3(self) -> None:
        self.safe_click(self.step3_dropdown)

    def get_account_id(self) -> str:
        self.safe_click(self.account_id_copy_button)
        return self.read_clipboard()

    def get_external_id(self) -> str:
        self.safe_click(self.external_id_copy_button)
        return self.read_clipboard()

    def paste_role_arn(self) -> None:
        self.safe_click(self.role_arn_input)
        self.page.keyboard.press("Control+V")
        expect(self.role_arn_input).not_to_have_value("", timeout=DEFAULT)

    # =========================================================================
    # STEP 4 — CORS
    # =========================================================================

    def open_step_4(self) -> None:
        self.wait.for_visible(self.step4_dropdown)
        self.safe_click(self.step4_dropdown)

    def copy_cors_json(self) -> str:
        copy_button = self.page.get_by_role("button", name="Copy").nth(3)
        self.wait.for_visible(copy_button)
        self.safe_click(copy_button)
        return self.read_clipboard(expected_prefix="[")

    # =========================================================================
    # CREATE / VALIDATE
    # =========================================================================

    def click_create_integration(self) -> None:
        self.wait.for_visible(self.create_button)
        self.safe_click(self.create_button)
        self.wait.for_hidden(self.create_button, timeout=LONG)

    # =========================================================================
    # RUN A TEST
    # =========================================================================

    def click_run_a_test(self) -> None:
        self.wait.for_visible(self.run_test_button)
        self.safe_click(self.run_test_button)

    def enter_s3_url(self, s3_url: str) -> None:
        self.safe_fill(self.test_url_input, s3_url)
        print(f"\nS3 URL entered: {s3_url}")

    def click_check_button(self) -> None:
        self.wait.for_visible(self.check_button)
        self.safe_click(self.check_button)
        print("\nCheck button clicked")