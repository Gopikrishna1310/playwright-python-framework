import re
import logging

from playwright.sync_api import Page, expect

from pages.common.base_page import BasePage
from utils.waits import DEFAULT, LOAD, LONG

logger = logging.getLogger(__name__)


class TemplatesPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.templates_menu          = page.get_by_role("link", name="Templates")
        self.upload_new_template_btn = page.get_by_role("button", name="Upload New Template")
        self.template_name_textbox   = page.get_by_role(
            "textbox", name="Template Name * Upload file *"
        )
        self.delete_confirm_textbox  = page.get_by_role("textbox")

    # =========================================================================
    # OPEN TEMPLATES PAGE
    # =========================================================================

    def open_templates_page(self) -> None:
        self.safe_click(self.templates_menu)
        self.wait.for_url_contains("/templates", timeout=LOAD)
        logger.info("[TemplatesPage] Templates page opened")

    # =========================================================================
    # ASSERTIONS
    # =========================================================================

    def verify_templates_page_opened(self) -> None:
        # $ anchor — /templates/9 also contains /templates as substring
        expect(self.page).to_have_url(
            re.compile(r"/templates$"), timeout=LONG
        )
        self.verify_visible(self.upload_new_template_btn, timeout=LONG)
        logger.info(
            f"[TemplatesPage]  Templates page verified: {self.page.url}"
        )

    def verify_template_visible(self, template_name: str) -> None:
        self.verify_visible(
            self.page.get_by_text(template_name).first, timeout=LONG
        )
        logger.info(f"[TemplatesPage]  Template visible: {template_name}")

    def verify_template_not_visible(self, template_name: str) -> None:
        template_row = self.page.get_by_role(
            "row",
            name=re.compile(re.escape(template_name), re.IGNORECASE)
        )
        self.verify_count(template_row, 0, timeout=LONG)
        logger.info(f"[TemplatesPage]  Template not visible: {template_name}")

    # =========================================================================
    # UPLOAD TEMPLATE
    # =========================================================================

    def open_upload_template_popup(self) -> None:
        self.safe_click(self.upload_new_template_btn)
        self.wait.for_visible(self.template_name_textbox)
        logger.info("[TemplatesPage] Upload Template popup opened")

    def enter_template_name(self, template_name: str) -> None:
        self.safe_fill(self.template_name_textbox, template_name)
        logger.info(f"[TemplatesPage] Template name entered: {template_name}")

    def upload_template_file(self, file_path: str) -> None:
        assert file_path.endswith(".zip"), (
            f"Template file must be a .zip — got: {file_path}"
        )
        self.page.locator('input[type="file"]').set_input_files(file_path)
        logger.info(f"[TemplatesPage]  Template file verified as .zip and selected: {file_path}")

    def click_upload_template_button(self) -> None:
        self.safe_click(self.page.get_by_role("button", name="Upload"))
        self.wait.for_hidden(self.template_name_textbox, timeout=LONG)
        logger.info("[TemplatesPage] Template uploaded — modal closed")

    def upload_template(self, template_name: str, file_path: str) -> None:
        self.open_upload_template_popup()
        self.enter_template_name(template_name)
        self.upload_template_file(file_path)
        self.click_upload_template_button()
        logger.info(f"[TemplatesPage] Template upload complete: {template_name}")

    # =========================================================================
    # DELETE TEMPLATE
    # =========================================================================

    def select_template_checkbox(self, template_name: str) -> None:
        template_row = self.page.get_by_role(
            "row",
            name=re.compile(re.escape(template_name), re.IGNORECASE)
        ).first
        self.wait.for_visible(template_row, timeout=LONG)
        template_row.get_by_role("checkbox").check()
        logger.info(f"[TemplatesPage] Template selected: {template_name}")

    def click_delete_template_button(self) -> None:
        self.safe_click(self.page.get_by_role("button", name="Delete"))
        self.wait.for_visible(self.delete_confirm_textbox)
        logger.info("[TemplatesPage] Delete button clicked — confirmation dialog ready")

    def enter_template_delete_confirmation(self) -> None:
        self.safe_fill(self.delete_confirm_textbox, "DELETE")
        logger.info("[TemplatesPage] DELETE confirmation entered")

    def confirm_template_delete(self) -> None:
        self.safe_click(self.page.get_by_role("button", name="Delete").last)
        self.wait.for_hidden(self.delete_confirm_textbox, timeout=LONG)
        logger.info("[TemplatesPage] Delete confirmed")

    def close_delete_summary_popup(self) -> None:
        close_button = (
            self.page.locator("button")
            .filter(has=self.page.locator("svg"))
            .last
        )
        self.safe_click(close_button)
        self.wait.for_page_ready()
        logger.info("[TemplatesPage] Delete summary popup closed")