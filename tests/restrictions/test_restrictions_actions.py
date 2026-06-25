import logging
import pytest

from pages.common.login_page import LoginPage
from pages.common.sidebar_page import SidebarPage
from pages.restrictions.restrictions_page import RestrictionsPage
from config.credentials import TOOL_EMAIL, TOOL_PASSWORD

logger = logging.getLogger(__name__)


@pytest.mark.restrictions
def test_restrictions_actions(page):

    # =========================================================================
    # LOGIN
    # =========================================================================

    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(TOOL_EMAIL, TOOL_PASSWORD)

    sidebar_page = SidebarPage(page)
    sidebar_page.select_organization_and_role()

    restrictions_page = RestrictionsPage(page)

    # =========================================================================
    # TC_09_01: Workflow delete restriction
    # =========================================================================

    # When: Navigate to Workflows page
    restrictions_page.open_workflows_page()

    # Then: Verify on Workflows page
    restrictions_page.verify_page_url("/workflows")
    logger.info("TC_09_01 Workflows page verified")

    # When: Select workflow and attempt delete
    restrictions_page.attempt_delete_workflow("Testing workflow 1")

    # Then: Restriction message should appear
    restrictions_page.verify_restriction_message("Failed Deleted Workflow")

    restrictions_page.close_popup()

    # Then: Workflow should still be in the list
    restrictions_page.verify_item_still_in_list("Testing workflow 1")
    logger.info("TC_09_01 Workflow restriction verified — workflow still in list")

    # =========================================================================
    # TC_09_02: Template delete restriction
    # =========================================================================

    # When: Navigate to Templates page
    restrictions_page.open_templates_page()

    # Then: Verify on Templates page
    restrictions_page.verify_page_url("/templates")
    logger.info("TC_09_02 Templates page verified")

    # When: Select template and attempt delete
    restrictions_page.attempt_delete_template("Test template - 1")

    # Then: Restriction message should appear
    restrictions_page.verify_restriction_message("Failed Deleted Template")

    restrictions_page.close_popup()

    # Then: Template should still be in the list
    restrictions_page.verify_item_still_in_list("Test template - 1")
    logger.info("TC_09_02 Template restriction verified — template still in list")

    # =========================================================================
    # TC_09_03: Dataset delete restriction
    # =========================================================================

    # When: Navigate to Datasets page
    restrictions_page.open_datasets_page()

    # Then: Verify on Datasets page
    restrictions_page.verify_page_url("/datasets")
    logger.info("TC_09_03 Datasets page verified")

    # When: Select dataset and attempt delete
    restrictions_page.attempt_delete_dataset("Test 3")

    # Then: Restriction message should appear
    restrictions_page.verify_restriction_message("Failed Deleted Dataset")

    restrictions_page.close_popup()

    # Then: Dataset should still be in the list
    restrictions_page.verify_item_still_in_list("Test 3")
    logger.info("TC_09_03 Dataset restriction verified — dataset still in list")

    # =========================================================================
    # TC_09_04: Dataset file delete restriction
    # =========================================================================

    # When: Open dataset and attempt to delete files
    restrictions_page.open_dataset("Test 3")

    restrictions_page.attempt_delete_dataset_files([
        "Copy - Copy.wav",
        "audio 4.wav"
    ])

    # Then: Restriction message should appear
    restrictions_page.verify_restriction_message("Failed Detached Files")

    restrictions_page.close_popup()

    # Then: Files should still be in the dataset
    restrictions_page.verify_files_still_in_list([
        "Copy - Copy.wav",
        "audio 4.wav"
    ])
    logger.info("TC_09_04 Dataset file restriction verified — files still in dataset")

    # =========================================================================
    # TC_09_05: Files page delete restriction
    # =========================================================================

    # When: Navigate to Files page
    restrictions_page.open_files_page()

    # Then: Verify on Files page
    restrictions_page.verify_page_url("/files")
    logger.info("TC_09_05 Files page verified")

    # When: Select files and attempt delete
    restrictions_page.attempt_delete_files([
        "Copy - Copy.wav",
        "audio 4.wav"
    ])

    # Then: Restriction message should appear
    restrictions_page.verify_restriction_message("Failed Deletions")

    restrictions_page.close_popup()

    # Then: Files should still be in the list
    restrictions_page.verify_files_still_in_list([
        "Copy - Copy.wav",
        "audio 4.wav"
    ])
    logger.info("TC_09_05 Files restriction verified — files still in list")

    # =========================================================================
    # TC_09_06: Integration delete restriction
    # =========================================================================

    # When: Navigate to Integrations page
    restrictions_page.open_integrations_page()

    # Then: Verify on Integrations page
    restrictions_page.verify_page_url("/s3-connections")
    logger.info("TC_09_06 Integrations page verified")

    # When: Select integration and attempt delete
    restrictions_page.attempt_delete_integration("Test")

    # Then: Restriction message should appear
    restrictions_page.verify_restriction_message("Failed Deleted Integration")

    restrictions_page.close_popup()

    # Then: Integration should still be in the list
    restrictions_page.verify_item_still_in_list("Test")
    logger.info("TC_09_06 Integration restriction verified — integration still in list")

    logger.info("Restriction regression completed successfully")