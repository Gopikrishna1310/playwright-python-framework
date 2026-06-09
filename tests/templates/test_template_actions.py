import pytest

from pages.common.login_page import LoginPage

from pages.templates.templates_page import TemplatesPage

from config.credentials import (
    TOOL_EMAIL,
    TOOL_PASSWORD
)


@pytest.mark.templates
def test_template_actions(page):

    # ============================================
    # LOGIN
    # ============================================

    login_page = LoginPage(page)

    login_page.open_login_page()

    login_page.login(
        TOOL_EMAIL,
        TOOL_PASSWORD
    )

    print(
        "\nLogin successful"
    )

    # ============================================
    # OPEN TEMPLATES PAGE
    # ============================================

    templates_page = TemplatesPage(page)

    templates_page.open_templates_page()

    templates_page.validate_templates_page_opened()

    print(
        "\nTC_05_01 Open Templates page completed"
    )

    # ============================================
    # TC_05_02
    # UPLOAD TEMPLATES
    # ============================================

    templates = [

        (
            "Test template - 1",
            "test_data/files/template/Updated Audio template.zip"
        ),

        (
            "Test Template -2",
            "test_data/files/template/Updated text template.zip"
        )
    ]

    for (
            template_name,
            file_path
    ) in templates:

        templates_page.upload_template(
            template_name,
            file_path
        )

        print(
            f"\nTemplate upload completed:\n{template_name}"
        )

    print(
        "\nTC_05_02 Upload Templates completed"
    )

    # ============================================
    # TC_05_03
    # DELETE TEMPLATES
    # ============================================

    delete_templates = [

        "Test Template -2"
    ]

    for template_name in delete_templates:

        templates_page.select_template_checkbox(
            template_name
        )

    templates_page.click_delete_template_button()

    templates_page.enter_template_delete_confirmation()

    templates_page.confirm_template_delete()

    templates_page.close_delete_summary_popup()

    print(
        "\nTC_05_03 Delete Templates completed"
    )