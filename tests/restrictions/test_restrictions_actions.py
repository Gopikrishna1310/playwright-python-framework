import pytest

from pages.common.login_page import LoginPage
from pages.common.sidebar_page import SidebarPage

from pages.restrictions.restrictions_page import (
    RestrictionsPage
)

from config.credentials import (
    TOOL_EMAIL,
    TOOL_PASSWORD
)


@pytest.mark.restrictions
def test_restrictions_actions(page):

    # ============================================
    # LOGIN
    # ============================================

    login_page = LoginPage(page)

    login_page.open_login_page()

    login_page.login(
        TOOL_EMAIL,
        TOOL_PASSWORD
    )

    # ============================================
    # ORGANIZATION + ROLE
    # ============================================

    sidebar_page = SidebarPage(page)

    sidebar_page.select_organization_and_role()

    print(
        "\nLogin successful"
    )

    # ============================================
    # PAGE OBJECT
    # ============================================

    restrictions_page = RestrictionsPage(page)

    # ============================================
    # TC_09_01
    # WORKFLOW DELETE RESTRICTION
    # ============================================

    restrictions_page.open_workflows_page()

    restrictions_page.attempt_delete_workflow(
        "Testing workflow 1"
    )

    restrictions_page.validate_restriction_message(
        "Failed Deleted Workflow"
    )

    restrictions_page.close_popup()

    print(
        "\nTC_09_01 Workflow restriction validated"
    )

    # ============================================
    # TC_09_02
    # TEMPLATE DELETE RESTRICTION
    # ============================================

    restrictions_page.open_templates_page()

    restrictions_page.attempt_delete_template(
        "Test template - 1"
    )

    restrictions_page.validate_restriction_message(
        "Failed Deleted Template"
    )

    restrictions_page.close_popup()

    print(
        "\nTC_09_02 Template restriction validated"
    )

    # ============================================
    # TC_09_03
    # DATASET DELETE RESTRICTION
    # ============================================

    restrictions_page.open_datasets_page()

    restrictions_page.attempt_delete_dataset(
        "Test 3"
    )

    restrictions_page.validate_restriction_message(
        "Failed Deleted Dataset"
    )

    restrictions_page.close_popup()

    print(
        "\nTC_09_03 Dataset restriction validated"
    )

    # ============================================
    # TC_09_04
    # DATASET FILE DELETE RESTRICTION
    # ============================================

    restrictions_page.open_dataset(
        "Test 3"
    )

    restrictions_page.attempt_delete_dataset_files(
        [
            "Copy - Copy.wav",
            "audio 4.wav"
        ]
    )

    restrictions_page.validate_restriction_message(
        "Failed Detached Files"
    )

    restrictions_page.close_popup()

    print(
        "\nTC_09_04 Dataset file restriction validated"
    )

    # ============================================
    # TC_09_05
    # FILE DELETE RESTRICTION
    # ============================================

    restrictions_page.open_files_page()

    restrictions_page.attempt_delete_files(
        [
            "Copy - Copy.wav",
            "audio 4.wav"
        ]
    )

    restrictions_page.validate_restriction_message(
        "Failed Deletions"
    )

    restrictions_page.close_popup()

    print(
        "\nTC_09_05 Files restriction validated"
    )

    # ============================================
    # TC_09_06
    # INTEGRATION DELETE RESTRICTION
    # ============================================

    restrictions_page.open_integrations_page()

    restrictions_page.attempt_delete_integration(
        "Test"
    )

    restrictions_page.validate_restriction_message(
        "Failed Deleted Integration"
    )

    restrictions_page.close_popup()

    print(
        "\nTC_09_06 Integration restriction validated"
    )

    # ============================================
    # FINAL MESSAGE
    # ============================================

    print(
        "\nRestriction regression completed successfully"
    )