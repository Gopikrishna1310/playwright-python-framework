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

from pages.integrations.s3_integration_page import (
    S3IntegrationPage
)

from pages.aws.aws_login_page import (
    AWSLoginPage
)

from pages.aws.aws_iam_page import (
    AWSIAMPage
)

from pages.aws.aws_role_page import (
    AWSRolePage
)

from pages.aws.aws_s3_page import (
    AWSS3Page
)


@pytest.mark.s3
def test_full_s3_integration_flow(page):

    # ============================================
    # LOGIN TO TOOL
    # ============================================

    login_page = LoginPage(page)

    login_page.open_login_page()

    login_page.login(
        TOOL_EMAIL,
        TOOL_PASSWORD
    )

    print("\nLogin successful")

    # ============================================
    # OPEN INTEGRATIONS PAGE
    # ============================================

    sidebar_page = SidebarPage(page)

    sidebar_page.open_integrations_page()

    current_url = page.url

    print(f"\nCurrent URL: {current_url}")

    assert "s3-connections" in current_url

    print("\nIntegrations page opened successfully")

    # ============================================
    # OPEN S3 POPUP
    # ============================================

    s3_page = S3IntegrationPage(page)

    s3_page.open_new_integration_popup()

    print("\nS3 Integration popup opened")

    # ============================================
    # ENTER BASIC DETAILS
    # ============================================

    s3_page.enter_basic_details(
        INTEGRATION_TITLE,
        S3_BUCKET_NAME
    )

    print(
        "\nIntegration details entered successfully"
    )

    # ============================================
    # OPEN STEP 2
    # ============================================

    s3_page.open_step_2()

    print(
        "\nStep 2 opened successfully"
    )

    # ============================================
    # GET REAL POLICY JSON
    # ============================================

    policy_json = s3_page.get_policy_json()

    print(
        "\nReal policy JSON captured"
    )

    # ============================================
    # OPEN AWS PAGE
    # ============================================

    # IMPORTANT:
    # Use SAME browser context
    # so clipboard permissions are shared

    aws_page_tab = (
        page.context.new_page()
    )

    # ============================================
    # AWS LOGIN
    # ============================================

    aws_login_page = AWSLoginPage(
        aws_page_tab
    )

    aws_login_page.open_aws_login_page()

    aws_login_page.login_to_aws(
        AWS_ACCOUNT,
        AWS_USERNAME,
        AWS_PASSWORD
    )

    print(
        "\nAWS Login Successful"
    )

    # ============================================
    # IAM PAGE
    # ============================================

    iam_page = AWSIAMPage(
        aws_page_tab
    )

    # ============================================
    # OPEN IAM CONSOLE
    # ============================================

    iam_page.open_iam_console()

    print(
        "\nIAM Console opened"
    )

    # ============================================
    # OPEN POLICIES PAGE
    # ============================================

    iam_page.open_policies_page()

    print(
        "\nPolicies page opened"
    )

    # ============================================
    # SEARCH POLICY
    # ============================================

    iam_page.search_policy(
        S3_BUCKET_NAME
    )

    print(
        "\nPolicy searched successfully"
    )

    # ============================================
    # OPEN POLICY
    # ============================================

    iam_page.open_policy(
        S3_BUCKET_NAME
    )

    print(
        "\nPolicy opened successfully"
    )

    # ============================================
    # CLICK EDIT POLICY
    # ============================================

    iam_page.click_edit_policy()

    print(
        "\nEdit Policy screen opened"
    )

    # ============================================
    # REPLACE REAL POLICY JSON
    # ============================================

    iam_page.replace_policy_json(
        policy_json
    )

    print(
        "\nReal policy JSON replaced successfully"
    )

    # ============================================
    # SAVE POLICY
    # ============================================

    iam_page.save_policy()

    print(
        "\nPolicy saved successfully"
    )

    # ============================================
    # OPEN STEP 3
    # ============================================

    s3_page.open_step_3()

    print(
        "\nStep 3 opened successfully"
    )

    # ============================================
    # GET ACCOUNT ID
    # ============================================

    account_id = s3_page.get_account_id()

    print(
        f"\nAccount ID: {account_id}"
    )

    # ============================================
    # GET EXTERNAL ID
    # ============================================

    external_id = s3_page.get_external_id()

    print(
        f"\nExternal ID: {external_id}"
    )

    # ============================================
    # AWS ROLE PAGE
    # ============================================

    role_page = AWSRolePage(
        aws_page_tab
    )

    # ============================================
    # OPEN ROLES PAGE
    # ============================================

    role_page.open_roles_page()

    print(
        "\nRoles page opened"
    )

    # ============================================
    # CLICK CREATE ROLE
    # ============================================

    role_page.click_create_role()

    print(
        "\nCreate Role page opened"
    )

    # ============================================
    # SELECT AWS ACCOUNT
    # ============================================

    role_page.select_aws_account()

    # ============================================
    # SELECT ANOTHER AWS ACCOUNT
    # ============================================

    role_page.select_another_aws_account()

    # ============================================
    # ENTER ACCOUNT ID
    # ============================================

    role_page.enter_account_id(
        account_id
    )

    # ============================================
    # ENABLE EXTERNAL ID
    # ============================================

    role_page.enable_external_id()

    # ============================================
    # ENTER EXTERNAL ID
    # ============================================

    role_page.enter_external_id(
        external_id
    )

    # ============================================
    # GO TO PERMISSIONS PAGE
    # ============================================

    role_page.go_to_permissions_page()

    # ============================================
    # ATTACH POLICY
    # ============================================

    role_page.attach_policy(
        S3_BUCKET_NAME
    )

    # ============================================
    # ENTER ROLE NAME
    # ============================================

    role_page.enter_role_name(
        ROLE_NAME
    )

    # ============================================
    # CREATE ROLE
    # ============================================

    role_page.create_role()

    # ============================================
    # OPEN CREATED ROLE
    # ============================================

    role_page.open_created_role(
        ROLE_NAME
    )

    # ============================================
    # COPY ROLE ARN
    # ============================================

    role_page.copy_role_arn()

    # ============================================
    # RETURN TO FM TOOL
    # ============================================

    s3_page.switch_to_page(page)

    print(
        "\nReturned to FM Tool"
    )

    # ============================================
    # PASTE ROLE ARN
    # ============================================

    s3_page.paste_role_arn()

    # ============================================
    # OPEN STEP 4
    # ============================================

    s3_page.open_step_4()

    # ============================================
    # COPY CORS JSON
    # ============================================

    cors_json = s3_page.copy_cors_json()

    print(
        f"\nCORS JSON:\n{cors_json}"
    )

    # ============================================
    # AWS S3 PAGE
    # ============================================

    s3_aws_page = AWSS3Page(
        aws_page_tab
    )

    # ============================================
    # OPEN S3 CONSOLE
    # ============================================

    s3_aws_page.open_s3_console()

    # ============================================
    # SEARCH BUCKET
    # ============================================

    s3_aws_page.search_bucket(
        S3_BUCKET_NAME
    )

    # ============================================
    # OPEN BUCKET
    # ============================================

    s3_aws_page.open_bucket(
        S3_BUCKET_NAME
    )

    # ============================================
    # OPEN PERMISSIONS TAB
    # ============================================

    s3_aws_page.open_permissions_tab()

    # ============================================
    # CLICK EDIT CORS
    # ============================================

    s3_aws_page.click_edit_cors()

    # ============================================
    # REPLACE CORS JSON
    # ============================================

    s3_aws_page.replace_cors_json(
        cors_json
    )

    # ============================================
    # SAVE CHANGES
    # ============================================

    s3_aws_page.save_changes()
    # ============================================
    # RETURN TO FM TOOL
    # ============================================

    s3_page.switch_to_page(page)

    print(
        "\nReturned to FM Tool"
    )

    # ============================================
    # CLICK CREATE INTEGRATION
    # ============================================

    s3_page.click_create_integration()

    # ============================================
    # VALIDATE SUCCESS
    # ============================================

    s3_page.validate_integration_created()
    # ============================================
    # OPEN RUN TEST POPUP
    # ============================================

    s3_page.click_run_a_test()

    # ============================================
    # AWS OBJECTS TAB
    # ============================================

    s3_aws_page.open_objects_tab()

    # ============================================
    # OPEN FILE
    # ============================================

    s3_aws_page.open_first_file()

    # ============================================
    # COPY S3 URI
    # ============================================

    s3_uri = s3_aws_page.copy_s3_uri()

    # ============================================
    # RETURN TO FM TOOL
    # ============================================

    s3_page.switch_to_page(page)

    # ============================================
    # ENTER S3 URL
    # ============================================

    s3_page.enter_s3_url(
        s3_uri
    )

    # ============================================
    # CLICK CHECK BUTTON
    # ============================================

    s3_page.click_check_button()

    # ============================================
    # VALIDATE TEST SUCCESS
    # ============================================

    s3_page.validate_test_success()