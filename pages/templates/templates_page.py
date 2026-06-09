import re

from playwright.sync_api import Page

from pages.common.base_page import BasePage


class TemplatesPage(BasePage):

    def __init__(
            self,
            page: Page
    ):

        super().__init__(page)

        self.templates_menu = page.get_by_role(
            "link",
            name="Templates"
        )

    # ============================================
    # OPEN TEMPLATES PAGE
    # ============================================

    def open_templates_page(self):

        self.safe_click(
            self.templates_menu
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nTemplates page opened"
        )

    # ============================================
    # VALIDATE TEMPLATES PAGE
    # ============================================

    def validate_templates_page_opened(self):

        self.page.wait_for_url(
            "**/templates",
            timeout=60000
        )

        print(
            f"\nCurrent URL: {self.page.url}"
        )

        print(
            "\nTemplates page validation successful"
        )

    # ============================================
    # OPEN UPLOAD TEMPLATE POPUP
    # ============================================

    def open_upload_template_popup(self):

        upload_button = self.page.get_by_role(
            "button",
            name="Upload New Template"
        )

        self.safe_click(
            upload_button
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nUpload Template popup opened"
        )

    # ============================================
    # ENTER TEMPLATE NAME
    # ============================================

    def enter_template_name(
            self,
            template_name
    ):

        textbox = self.page.get_by_role(
            "textbox",
            name="Template Name * Upload file *"
        )

        self.safe_fill(
            textbox,
            template_name
        )

        self.page.wait_for_timeout(1000)

        print(
            f"\nTemplate name entered:\n{template_name}"
        )

    # ============================================
    # UPLOAD TEMPLATE FILE
    # ============================================

    def upload_template_file(
            self,
            file_path
    ):

        file_input = self.page.locator(
            'input[type="file"]'
        )

        file_input.set_input_files(
            file_path
        )

        # Upload stabilization
        self.page.wait_for_timeout(3000)

        print(
            f"\nTemplate file uploaded:\n{file_path}"
        )

    # ============================================
    # CLICK UPLOAD BUTTON
    # ============================================

    def click_upload_template_button(self):

        upload_button = self.page.get_by_role(
            "button",
            name="Upload"
        )

        self.safe_click(
            upload_button
        )

        # Backend template processing
        self.page.wait_for_timeout(5000)

        print(
            "\nTemplate upload confirmed"
        )

    # ============================================
    # VALIDATE TEMPLATE CREATED
    # ============================================

    def validate_template_created(
            self,
            template_name
    ):

        template = self.page.get_by_text(
            template_name
        ).first

        template.wait_for(
            state="visible",
            timeout=60000
        )

        print(
            f"\nTemplate validated:\n{template_name}"
        )

    # ============================================
    # COMPLETE TEMPLATE UPLOAD FLOW
    # ============================================

    def upload_template(
            self,
            template_name,
            file_path
    ):

        self.open_upload_template_popup()

        self.enter_template_name(
            template_name
        )

        self.upload_template_file(
            file_path
        )

        self.click_upload_template_button()

        self.validate_template_created(
            template_name
        )

    # ============================================
    # SELECT TEMPLATE CHECKBOX
    # ============================================

    def select_template_checkbox(
            self,
            template_name
    ):

        template_row = self.page.get_by_role(
            "row",
            name=re.compile(
                re.escape(template_name),
                re.IGNORECASE
            )
        ).first

        template_row.wait_for(
            state="visible",
            timeout=60000
        )

        checkbox = template_row.get_by_role(
            "checkbox"
        )

        checkbox.check()

        self.page.wait_for_timeout(1500)

        print(
            f"\nTemplate selected:\n{template_name}"
        )

    # ============================================
    # CLICK DELETE BUTTON
    # ============================================

    def click_delete_template_button(self):

        delete_button = self.page.get_by_role(
            "button",
            name="Delete"
        )

        self.safe_click(
            delete_button
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nTemplate delete button clicked"
        )

    # ============================================
    # ENTER DELETE CONFIRMATION
    # ============================================

    def enter_template_delete_confirmation(self):

        textbox = self.page.get_by_role(
            "textbox"
        )

        self.safe_fill(
            textbox,
            "DELETE"
        )

        self.page.wait_for_timeout(1000)

        print(
            "\nTemplate DELETE confirmation entered"
        )

    # ============================================
    # CONFIRM TEMPLATE DELETE
    # ============================================

    def confirm_template_delete(self):

        confirm_button = (
            self.page
            .get_by_role(
                "button",
                name="Delete"
            )
            .last
        )

        self.safe_click(
            confirm_button
        )

        # Backend delete propagation
        self.page.wait_for_timeout(5000)

        print(
            "\nTemplate delete confirmed"
        )

    # ============================================
    # CLOSE DELETE SUMMARY POPUP
    # ============================================

    def close_delete_summary_popup(self):

        close_button = (
            self.page
            .locator("button")
            .filter(
                has=self.page.locator("svg")
            )
            .last
        )

        self.safe_click(
            close_button
        )

        self.page.wait_for_timeout(1500)

        print(
            "\nTemplate delete summary popup closed"
        )