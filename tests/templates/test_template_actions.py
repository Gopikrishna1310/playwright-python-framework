import logging
import pytest

from pages.common.login_page import LoginPage
from pages.templates.templates_page import TemplatesPage
from config.credentials import TOOL_EMAIL, TOOL_PASSWORD

logger = logging.getLogger(__name__)


@pytest.mark.templates
def test_template_actions(page):

    # =========================================================================
    # LOGIN
    # =========================================================================

    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(TOOL_EMAIL, TOOL_PASSWORD)

    # =========================================================================
    # TC_05_01: Open Templates page
    # =========================================================================

    templates_page = TemplatesPage(page)

    # When: Click Templates from sidebar
    templates_page.open_templates_page()

    # Then: Templates list page should open
    templates_page.verify_templates_page_opened()
    logger.info("TC_05_01 Templates page opened and verified")

    # =========================================================================
    # TC_05_02: Upload templates
    # =========================================================================

    templates = [
        (
            "Test template - 1",
            "test_data/files/template/Updated Audio template.zip"
        ),
        (
            "Test Template -2",
            "test_data/files/template/Updated text template.zip"
        ),
    ]

    for template_name, file_path in templates:

        # When: Click Upload New Template and fill name
        templates_page.open_upload_template_popup()
        templates_page.enter_template_name(template_name)

        # When: Select template file
        # Then: File must be in .zip format (asserted inside upload_template_file)
        templates_page.upload_template_file(file_path)

        # When: Click Upload
        templates_page.click_upload_template_button()

        # Then: Template should be visible in the list
        templates_page.verify_template_visible(template_name)
        logger.info(f"TC_05_02 Template uploaded and verified: {template_name}")

    logger.info("TC_05_02 All templates uploaded successfully")

    # =========================================================================
    # TC_05_03: Delete template
    # =========================================================================

    delete_templates = ["Test Template -2"]

    for template_name in delete_templates:
        # When: Select template checkbox
        templates_page.select_template_checkbox(template_name)

    # When: Click Delete, confirm with DELETE text
    templates_page.click_delete_template_button()
    templates_page.enter_template_delete_confirmation()
    templates_page.confirm_template_delete()
    templates_page.close_delete_summary_popup()

    # Then: Deleted template should not be visible
    for template_name in delete_templates:
        templates_page.verify_template_not_visible(template_name)
        logger.info(f"TC_05_03 Template deleted and verified not visible: {template_name}")

    logger.info("TC_05_03 Delete Templates completed")