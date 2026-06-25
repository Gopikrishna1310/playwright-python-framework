import re
import logging

from playwright.sync_api import Page

from pages.common.base_page import BasePage
from utils.waits import SHORT, DEFAULT, LONG, LOAD

logger = logging.getLogger(__name__)


class DatasetsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.datasets_menu          = page.get_by_role("link", name="Datasets")
        self.create_dataset_button  = page.get_by_role("button", name="Create Dataset")
        self.datasets_heading       = page.get_by_role("heading", name="Datasets")

        self._pending_dataset_deletes = []
        self._pending_file_deletes    = []

    # =========================================================================
    # PRIVATE HELPERS
    # =========================================================================

    def _row(self, name):
        return self.page.get_by_role(
            "row",
            name=re.compile(re.escape(name), re.IGNORECASE),
        )

    def _dialog(self):
        dialog = self.page.get_by_role("dialog")
        try:
            self.wait.for_visible(dialog.first, timeout=DEFAULT)
            return dialog.first
        except Exception:
            return self.page

    def _close_summary_popup(self):
        candidates = self.page.locator("div[role='dialog'] button")
        n = candidates.count()
        for i in range(n - 1, -1, -1):
            btn = candidates.nth(i)
            try:
                if btn.is_visible() and btn.is_enabled():
                    btn.click(timeout=SHORT)
                    logger.info("[DatasetsPage] Popup closed")
                    return
            except Exception:
                continue
        logger.info("[DatasetsPage] No popup to close — continuing")

    # =========================================================================
    # OPEN DATASETS PAGE
    # =========================================================================

    def open_datasets_page(self) -> None:
        self.safe_click(self.datasets_menu)
        self.wait.for_url_contains("/datasets", timeout=LOAD)
        logger.info("[DatasetsPage] Datasets page opened")

    # =========================================================================
    # ASSERTIONS
    # =========================================================================

    def verify_datasets_page_opened(self) -> None:
        # Must match exactly /datasets — not /datasets/9 (a dataset detail
        # page). re.escape("/datasets") would match both since it's a
        # substring. The $ anchor ensures the URL ends at /datasets.
        from playwright.sync_api import expect
        import re
        expect(self.page).to_have_url(
            re.compile(r"/datasets$"), timeout=DEFAULT
        )
        self.verify_visible(self.create_dataset_button, timeout=LONG)
        logger.info(f"[DatasetsPage]  Datasets page verified: {self.page.url}")

    def verify_dataset_visible(self, dataset_name: str) -> None:
        self.verify_visible(
            self.page.get_by_text(dataset_name).first, timeout=LONG
        )
        logger.info(f"[DatasetsPage]  Dataset visible: {dataset_name}")

    def verify_dataset_not_visible(self, dataset_name: str) -> None:
        self.verify_count(self._row(dataset_name), 0, timeout=LONG)
        logger.info(f"[DatasetsPage]  Dataset not visible: {dataset_name}")

    def verify_file_in_dataset(self, file_name: str) -> None:
        self.verify_visible(
            self.page.get_by_text(file_name).first, timeout=LONG
        )
        logger.info(f"[DatasetsPage]  File visible in dataset: {file_name}")

    def verify_file_not_in_dataset(self, file_name: str) -> None:
        self.verify_count(self._row(file_name), 0, timeout=LONG)
        logger.info(f"[DatasetsPage]  File removed from dataset: {file_name}")

    # =========================================================================
    # CREATE DATASET
    # =========================================================================

    def open_create_dataset_popup(self) -> None:
        self.safe_click(self.create_dataset_button)
        self.wait.for_visible(
            self.page.get_by_role("textbox", name="Enter Dataset Name"),
            timeout=DEFAULT,
        )
        logger.info("[DatasetsPage] Create Dataset popup opened")

    def enter_dataset_name(self, dataset_name: str) -> None:
        self.safe_fill(
            self.page.get_by_role("textbox", name="Enter Dataset Name"),
            dataset_name
        )
        logger.info(f"[DatasetsPage] Dataset name entered: {dataset_name}")

    def enter_dataset_description(self, description: str) -> None:
        description_input = self.page.get_by_role(
            "textbox", name="Enter Dataset Description"
        )
        if description_input.count() > 0:
            self.safe_fill(description_input, description)
            logger.info(f"[DatasetsPage] Description entered: {description}")

    def select_dataset_type(self, dataset_type: str) -> None:
        dropdown = self.page.get_by_role("button", name="Text")
        self.safe_click(dropdown)

        option = self.page.get_by_role("option", name=dataset_type, exact=True)
        if option.count() == 0:
            option = (
                self.page.locator("[data-floating-ui-portal]")
                .get_by_text(dataset_type, exact=True)
            )
        if option.count() == 0:
            option = (
                self.page.get_by_role("listbox")
                .get_by_text(dataset_type, exact=True)
            )

        self.wait.for_visible(option.first, timeout=DEFAULT)
        self.safe_click(option.first)
        logger.info(f"[DatasetsPage] Dataset type selected: {dataset_type}")

    def click_create_dataset_button(self) -> None:
        self.safe_click(self.page.get_by_role("button", name="Create"))
        try:
            self.wait.for_hidden(
                self.page.get_by_role("textbox", name="Enter Dataset Name"),
                timeout=LONG,
            )
        except Exception:
            pass
        logger.info("[DatasetsPage] Create dataset button clicked")

    def create_dataset(
        self, dataset_name: str, dataset_type: str, description: str = ""
    ) -> None:
        self.open_create_dataset_popup()
        self.enter_dataset_name(dataset_name)
        if dataset_type != "Text":
            self.select_dataset_type(dataset_type)
        if description:
            self.enter_dataset_description(description)
        self.click_create_dataset_button()

    # =========================================================================
    # OPEN DATASET / ADD FILES
    # =========================================================================

    def open_dataset(self, dataset_name: str) -> None:
        self.safe_click(self.page.get_by_text(dataset_name).first)
        self.wait.for_visible(
            self.page.get_by_role("button", name="Add Files"),
            timeout=LONG,
        )
        logger.info(f"[DatasetsPage] Dataset opened: {dataset_name}")

    def open_add_files_popup(self) -> None:
        self.safe_click(self.page.get_by_role("button", name="Add Files"))
        logger.info("[DatasetsPage] Add Files popup opened")

    def select_dataset_file(self, file_name: str) -> None:
        file_row = self._row(file_name).first
        self.wait.for_visible(file_row, timeout=LONG)
        self.safe_check(file_row.get_by_role("checkbox"))
        logger.info(f"[DatasetsPage] File selected: {file_name}")

    def click_add_files_button(self) -> None:
        self.safe_click(self.page.get_by_role("button", name="Add Files").last)
        logger.info("[DatasetsPage] Add Files confirmed")

    # =========================================================================
    # REMOVE FILES FROM DATASET
    # =========================================================================

    def select_dataset_file_checkbox(self, file_name: str) -> None:
        file_row = self._row(file_name).first
        self.wait.for_visible(file_row, timeout=LONG)
        self.safe_check(file_row.get_by_role("checkbox"))
        self._pending_file_deletes.append(file_name)
        logger.info(f"[DatasetsPage] File selected for delete: {file_name}")

    def click_delete_dataset_file_button(self) -> None:
        self.safe_click(self.page.get_by_role("button", name="Delete"))
        logger.info("[DatasetsPage] Dataset file delete button clicked")

    def enter_dataset_delete_confirmation(self) -> None:
        dialog = self._dialog()
        self.safe_fill(dialog.get_by_role("textbox"), "DELETE")
        logger.info("[DatasetsPage] DELETE confirmation entered")

    def confirm_dataset_file_delete(self) -> None:
        dialog = self._dialog()
        self.safe_click(dialog.get_by_role("button", name="Delete"))

        names = self._pending_file_deletes

        self.page.reload()
        self.wait.for_visible(
            self.page.get_by_role("button", name="Add Files"), timeout=LONG
        )

        for name in names:
            self.verify_count(self._row(name), 0, timeout=LONG)
            logger.info(f"[DatasetsPage]  File removed from dataset: {name}")

        self._pending_file_deletes = []
        logger.info("[DatasetsPage] Dataset file delete confirmed")

    def close_delete_summary_popup(self) -> None:
        self._close_summary_popup()

    # =========================================================================
    # DELETE DATASETS
    # =========================================================================

    def select_dataset_checkbox(self, dataset_name: str) -> None:
        dataset_row = self._row(dataset_name).first
        self.wait.for_visible(dataset_row, timeout=LONG)
        self.safe_check(dataset_row.get_by_role("checkbox"))
        self._pending_dataset_deletes.append(dataset_name)
        logger.info(f"[DatasetsPage] Dataset selected for delete: {dataset_name}")

    def click_delete_dataset_button(self) -> None:
        self.safe_click(self.page.get_by_role("button", name="Delete"))
        logger.info("[DatasetsPage] Dataset delete button clicked")

    def enter_dataset_confirmation(self) -> None:
        dialog = self._dialog()
        self.safe_fill(dialog.get_by_role("textbox"), "DELETE")
        logger.info("[DatasetsPage] Dataset DELETE confirmation entered")

    def confirm_dataset_delete(self, deleted_datasets=None) -> None:
        dialog = self._dialog()
        self.safe_click(dialog.get_by_role("button", name="Delete"))

        names = (
            deleted_datasets
            if deleted_datasets
            else self._pending_dataset_deletes
        )

        self.page.reload()
        self.wait.for_url_contains("/datasets", timeout=LOAD)

        for name in names:
            self.verify_count(self._row(name), 0, timeout=LONG)
            logger.info(f"[DatasetsPage]  Dataset deleted: {name}")

        self._pending_dataset_deletes = []
        self._close_summary_popup()
        logger.info("[DatasetsPage] Dataset delete confirmed")