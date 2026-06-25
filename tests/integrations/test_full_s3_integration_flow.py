import pytest

from config.credentials import (
    TOOL_EMAIL,
    TOOL_PASSWORD,
    AWS_ACCOUNT,
    AWS_USERNAME,
    AWS_PASSWORD
)

from config.test_data import (
    INTEGRATION_TITLE,
    S3_BUCKET_NAME,
    ROLE_NAME
)

from pages.common.login_page import LoginPage
from pages.common.sidebar_page import SidebarPage

from pages.integrations.s3_integration_page import S3IntegrationPage

from pages.aws.aws_login_page import AWSLoginPage
from pages.aws.aws_iam_page import AWSIAMPage
from pages.aws.aws_role_page import AWSRolePage
from pages.aws.aws_s3_page import AWSS3Page


@pytest.mark.s3
def test_full_s3_integration_flow(page):

    # =========================================================================
    # LOGIN TO TOOL
    # =========================================================================

    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(TOOL_EMAIL, TOOL_PASSWORD)

    # =========================================================================
    # TC_02_01: Open Integrations page
    # =========================================================================

    sidebar_page = SidebarPage(page)

    # When: Click Integrations from sidebar
    sidebar_page.open_integrations_page()

    # Then: Integrations list page should open
    assert "s3-connections" in page.url

    # =========================================================================
    # TC_02_02: Create a new S3 integration
    # =========================================================================

    s3_page = S3IntegrationPage(page)

    # When: Click New Integration button
    s3_page.open_new_integration_popup()

    # Then: Add S3 Integration popup should be displayed
    s3_page.verify_popup_opened()

    # When: Enter Integration Title and S3 Bucket Name
    s3_page.enter_basic_details(INTEGRATION_TITLE, S3_BUCKET_NAME)

    # When: Open Step 2
    s3_page.open_step_2()

    # Then: Generated JSON configuration should be displayed
    s3_page.verify_policy_json_visible()

    # When: Click Copy button
    policy_json = s3_page.get_policy_json()

    # Then: JSON should be copied successfully
    assert policy_json.startswith("{")

    # =========================================================================
    # AWS: IAM Policy
    # =========================================================================

    # IMPORTANT: same browser context — clipboard permissions are shared
    aws_page_tab = page.context.new_page()

    aws_login_page = AWSLoginPage(aws_page_tab)
    aws_login_page.open_aws_login_page()
    aws_login_page.login_to_aws(AWS_ACCOUNT, AWS_USERNAME, AWS_PASSWORD)

    iam_page = AWSIAMPage(aws_page_tab)
    iam_page.open_iam_console()
    iam_page.open_policies_page()
    iam_page.search_policy(S3_BUCKET_NAME)
    iam_page.open_policy(S3_BUCKET_NAME)
    iam_page.click_edit_policy()
    iam_page.replace_policy_json(policy_json)
    iam_page.save_policy()

    # =========================================================================
    # TOOL: Step 3 — IAM Role
    # =========================================================================

    # When: Open Step 3
    s3_page.open_step_3()

    # Then: Account ID and External ID fields should be visible
    s3_page.verify_account_external_id_fields_visible()

    # When: Copy Account ID and External ID
    account_id = s3_page.get_account_id()
    external_id = s3_page.get_external_id()

    assert account_id != ""
    assert external_id != ""

    # =========================================================================
    # AWS: IAM Role
    # =========================================================================

    role_page = AWSRolePage(aws_page_tab)
    role_page.open_roles_page()
    role_page.click_create_role()
    role_page.select_aws_account()
    role_page.select_another_aws_account()
    role_page.enter_account_id(account_id)
    role_page.enable_external_id()
    role_page.enter_external_id(external_id)
    role_page.go_to_permissions_page()
    role_page.attach_policy(S3_BUCKET_NAME)
    role_page.enter_role_name(ROLE_NAME)
    role_page.create_role()
    role_page.open_created_role(ROLE_NAME)
    role_page.copy_role_arn()

    # =========================================================================
    # TOOL: Paste ARN, Step 4 — CORS
    # =========================================================================

    s3_page.switch_to_page(page)

    # When: Paste Role ARN
    s3_page.paste_role_arn()

    # When: Open Step 4
    s3_page.open_step_4()

    # Then: CORS JSON configuration should be displayed
    s3_page.verify_cors_json_visible()

    # When: Click Copy button
    cors_json = s3_page.copy_cors_json()

    # Then: CORS JSON should be copied successfully
    assert cors_json.startswith("[")

    # =========================================================================
    # AWS: S3 Bucket CORS
    # =========================================================================

    s3_aws_page = AWSS3Page(aws_page_tab)
    s3_aws_page.open_s3_console()
    s3_aws_page.search_bucket(S3_BUCKET_NAME)
    s3_aws_page.open_bucket(S3_BUCKET_NAME)
    s3_aws_page.open_permissions_tab()
    s3_aws_page.click_edit_cors()
    s3_aws_page.replace_cors_json(cors_json)
    s3_aws_page.save_changes()

    # =========================================================================
    # TOOL: Create Integration
    # =========================================================================

    s3_page.switch_to_page(page)

    # When: Click Create button
    s3_page.click_create_integration()

    # Then: S3 integration should be created successfully
    s3_page.verify_integration_created()

    # Then: The integration should be visible in the list before proceeding
    s3_page.verify_integration_visible_in_list(integration_title=INTEGRATION_TITLE)

    # =========================================================================
    # TC_02_03: Run a test to verify the S3 integration
    # =========================================================================

    # When: Click Run a Test button
    s3_page.click_run_a_test()

    # Then: Test Integration popup should be displayed
    s3_page.verify_test_popup_opened()

    # =========================================================================
    # AWS: Get S3 object URL
    # =========================================================================

    s3_aws_page.open_objects_tab()
    s3_aws_page.open_first_file()
    s3_uri = s3_aws_page.copy_s3_uri()

    # =========================================================================
    # TOOL: Run the test
    # =========================================================================

    s3_page.switch_to_page(page)

    # When: Paste S3 URL and click Check
    s3_page.enter_s3_url(s3_uri)
    s3_page.click_check_button()

    # Then: Integration test should pass successfully
    s3_page.verify_test_success()