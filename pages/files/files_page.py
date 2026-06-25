import re
import logging

from playwright.sync_api import Page

from pages.common.base_page import BasePage
from utils.waits import DEFAULT, LONG, LOAD

logger = logging.getLogger(__name__)

FILES_URL = "https://fmn-qa.tensoract.com/files"
UPLOAD    = 120_000


class FilesPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.upload_files_button       = page.get_by_role("button", name="Upload Files")
        self.popup_upload_button       = page.get_by_role("button", name="Upload").nth(1)
        self.file_input                = page.locator('input[type="file"]')
        self.invalid_file_error        = page.get_by_text(
            "Invalid file type. Only allowed file types are permitted."
        )
        self.popup_close_button        = (
            page.get_by_role("button")
            .filter(has_text=re.compile(r"^$"))
            .last
        )
        self.upload_success_toast      = page.get_by_text(
            "Files uploaded successfully"
        )
        self.import_s3_button          = page.get_by_role("button", name="Import from S3")
        self.s3_integration_dropdown   = page.get_by_role("combobox")
        self.s3_picker_button          = page.get_by_role("button", name="Click to upload from S3")
        self.s3_upload_button          = page.get_by_role("button", name="Upload").first
        self.search_box                = page.get_by_placeholder("search")
        self.delete_button             = page.get_by_role("button", name="Delete")
        self.delete_confirmation_input = page.get_by_role("textbox")
        self.confirm_delete_button     = page.get_by_role("button", name="Delete").last

    # =========================================================================
    # PRIVATE HELPERS
    # =========================================================================

    def _file_row(self, file_name: str):
        return self.page.get_by_role(
            "row",
            name=re.compile(re.escape(file_name), re.IGNORECASE),
        )

    # =========================================================================
    # OPEN FILES PAGE
    # =========================================================================

    def open_files_page(self) -> None:
        self.open_url(FILES_URL)
        logger.info("[FilesPage] Files page opened")

    # =========================================================================
    # ASSERTIONS
    # =========================================================================

    def verify_files_page_opened(self) -> None:
        self.verify_url("/files")
        self.verify_visible(self.upload_files_button, timeout=LOAD)
        logger.info("[FilesPage]  Files page verified")

    def verify_upload_success(self) -> None:
        self.verify_visible(self.upload_success_toast, timeout=LONG)
        logger.info("[FilesPage]  Upload success toast visible")

    def verify_file_visible(self, file_name: str) -> None:
        self.verify_visible(self._file_row(file_name).first, timeout=UPLOAD)
        logger.info(f"[FilesPage]  File visible in table: {file_name}")

    def verify_file_not_visible(self, file_name: str) -> None:
        self.verify_count(self._file_row(file_name), 0, timeout=LONG)
        logger.info(f"[FilesPage]  File not in table: {file_name}")

    def verify_invalid_file_error(self) -> None:
        self.verify_visible(self.invalid_file_error, timeout=DEFAULT)
        logger.info("[FilesPage]  Invalid file error message visible")

    def verify_s3_integration_visible(self) -> None:
        self.verify_visible(self.s3_integration_dropdown, timeout=DEFAULT)
        logger.info("[FilesPage]  S3 integration dropdown visible")

    def verify_s3_integration_available(self) -> None:
        """
        Verifies the "Test" S3 integration option exists in the dropdown.
        Fails immediately with a clear message if not found.
        """
        self.verify_enabled(self.s3_integration_dropdown, timeout=DEFAULT)
        option = self.s3_integration_dropdown.locator("option", has_text="Test")
        assert option.count() > 0, (
            "TC_03_06 BLOCKED: 'Test' S3 integration not found in dropdown. "
            "Go to Integrations → verify the 'Test' S3 integration is configured."
        )
        logger.info("[FilesPage]  S3 integration 'Test' available")

    def verify_s3_files_visible(self, file_names: list) -> None:
        for file_name in file_names:
            self.verify_file_visible(file_name)
        logger.info(f"[FilesPage]  All S3 files visible: {file_names}")

    def verify_files_deleted(self, file_names: list) -> None:
        for file_name in file_names:
            self.verify_file_not_visible(file_name)
        logger.info(f"[FilesPage]  All files deleted: {file_names}")

    # =========================================================================
    # UPLOAD POPUP
    # =========================================================================

    def open_upload_files_popup(self) -> None:
        self.safe_click(self.upload_files_button)
        self.wait.for_visible(self.popup_upload_button)
        logger.info("[FilesPage] Upload popup opened")

    def upload_single_file(self, file_path: str) -> None:
        self.file_input.set_input_files(file_path)
        logger.info(f"[FilesPage] File attached: {file_path}")

    def upload_multiple_files(self, file_paths: list) -> None:
        self.file_input.set_input_files(file_paths)
        logger.info(f"[FilesPage] {len(file_paths)} files attached")

    def upload_invalid_file(self, file_path: str) -> None:
        self.file_input.set_input_files(file_path)
        logger.info(f"[FilesPage] Invalid file attached: {file_path}")

    def click_upload_button(self, expect_popup_close: bool = True) -> None:
        self.safe_click(self.popup_upload_button)
        if expect_popup_close:
            self.verify_hidden(self.popup_upload_button, timeout=UPLOAD)
        logger.info("[FilesPage] Upload button clicked")

    def close_upload_popup(self) -> None:
        self.safe_click(self.popup_close_button)
        self.verify_hidden(self.popup_upload_button, timeout=DEFAULT)
        logger.info("[FilesPage] Upload popup closed")

    # =========================================================================
    # S3 IMPORT
    # =========================================================================

    def open_import_from_s3(self) -> None:
        self.safe_click(self.import_s3_button)
        logger.info("[FilesPage] Import from S3 opened")

    def select_s3_integration(self) -> None:
        self.safe_select(self.s3_integration_dropdown, label="Test")
        logger.info("[FilesPage] S3 integration 'Test' selected")

    def open_s3_file_picker(self) -> None:
        self.safe_click(self.s3_picker_button)
        logger.info("[FilesPage] S3 file picker opened")

    def select_s3_files(self) -> None:
        rows = [19, 20, 21, 22]
        for row in rows:
            checkbox = self.page.locator(
                f"tr:nth-child({row}) > .px-3.py-2\\.5.w-16 > .rounded"
            )
            self.safe_check(checkbox)
        logger.info("[FilesPage] S3 files selected")

    def click_s3_upload_button(self) -> None:
        self.safe_click(self.s3_upload_button)
        self.wait.for_hidden(
            self.page.get_by_role("button", name="Uploading"),
            timeout=UPLOAD,
        )
        logger.info("[FilesPage] S3 import upload clicked")

    # =========================================================================
    # SEARCH
    # =========================================================================

    def search_file(self, file_name: str) -> None:
        self.safe_fill(self.search_box, file_name)
        logger.info(f"[FilesPage] Searched: {file_name}")

    def clear_search(self) -> None:
        self.search_box.clear(timeout=DEFAULT)
        logger.info("[FilesPage] Search cleared")

    # =========================================================================
    # SELECT / DELETE
    # =========================================================================

    def select_file_checkbox(self, file_name: str) -> None:
        self.search_file(file_name)
        file_row = self._file_row(file_name).first
        self.wait.for_visible(file_row, timeout=LONG)
        self.safe_check(file_row.get_by_role("checkbox"))
        self.clear_search()
        logger.info(f"[FilesPage] Selected: {file_name}")

    def click_delete_button(self) -> None:
        self.safe_click(self.delete_button)
        logger.info("[FilesPage] Delete button clicked")

    def enter_delete_confirmation(self) -> None:
        self.safe_fill(self.delete_confirmation_input, "DELETE")
        logger.info("[FilesPage] DELETE confirmation entered")

    def confirm_delete(self, deleted_files: list = None) -> None:
        self.safe_click(self.confirm_delete_button)
        if deleted_files:
            for file_name in deleted_files:
                self.verify_count(self._file_row(file_name), 0, timeout=LONG)
        else:
            self.wait.for_hidden(self.delete_confirmation_input, timeout=LONG)
        logger.info("[FilesPage] Delete confirmed")