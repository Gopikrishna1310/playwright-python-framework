import re
import logging

from playwright.sync_api import expect, Page

from pages.common.base_page import BasePage
from utils.waits import SHORT, DEFAULT, LONG, LOAD

logger = logging.getLogger(__name__)


class RestrictionsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # =========================================================================
    # PRIVATE
    # =========================================================================

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
                    logger.info("[RestrictionsPage] Popup closed")
                    return
            except Exception:
                continue
        logger.info("[RestrictionsPage] No popup to close — continuing")

    def _row(self, name: str):
        return self.page.get_by_role(
            "row", name=re.compile(re.escape(name))
        )

    # =========================================================================
    # NAVIGATION
    # =========================================================================

    def open_workflows_page(self) -> None:
        self.safe_click(self.page.get_by_role("link", name="Workflows"))
        self.wait.for_url_contains("/workflows", timeout=LOAD)
        logger.info("[RestrictionsPage] Workflows page opened")

    def open_templates_page(self) -> None:
        self.safe_click(self.page.get_by_role("link", name="Templates"))
        self.wait.for_url_contains("/templates", timeout=LOAD)
        logger.info("[RestrictionsPage] Templates page opened")

    def open_datasets_page(self) -> None:
        self.safe_click(self.page.get_by_role("link", name="Datasets"))
        self.wait.for_url_contains("/datasets", timeout=LOAD)
        logger.info("[RestrictionsPage] Datasets page opened")

    def open_files_page(self) -> None:
        self.safe_click(self.page.get_by_role("link", name="Files"))
        self.wait.for_url_contains("/files", timeout=LOAD)
        logger.info("[RestrictionsPage] Files page opened")

    def open_integrations_page(self) -> None:
        self.safe_click(self.page.get_by_role("link", name="Integrations"))
        self.wait.for_url_contains("/s3-connections", timeout=LOAD)
        logger.info("[RestrictionsPage] Integrations page opened")

    def open_dataset(self, dataset_name: str) -> None:
        self.safe_click(self.page.get_by_text(dataset_name, exact=True))
        logger.info(f"[RestrictionsPage] Dataset opened: {dataset_name}")

    # =========================================================================
    # ASSERTIONS
    # =========================================================================

    def verify_page_url(self, partial_url: str) -> None:
        self.verify_url(partial_url)
        logger.info(f"[RestrictionsPage]  Page verified: {self.page.url}")

    def verify_restriction_message(self, message: str) -> None:
        expect(
            self.page.get_by_text(message, exact=False)
        ).to_be_visible(timeout=LONG)
        logger.info(f"[RestrictionsPage]  Restriction message visible: {message}")

    def verify_item_still_in_list(self, name: str) -> None:
        self.verify_visible(self._row(name).first, timeout=LONG)
        logger.info(f"[RestrictionsPage]  Item still in list: {name}")

    def verify_files_still_in_list(self, file_names: list) -> None:
        for file_name in file_names:
            self.verify_visible(self._row(file_name).first, timeout=LONG)
            logger.info(f"[RestrictionsPage]  File still in list: {file_name}")

    # =========================================================================
    # COMMON DELETE FLOW
    # =========================================================================

    def perform_delete_confirmation(self) -> None:
        self.safe_click(self.page.get_by_role("button", name="Delete"))
        logger.info("[RestrictionsPage] Delete popup opened")

        dialog = self._dialog()
        confirm_input = dialog.get_by_role("textbox")
        self.wait.for_visible(confirm_input, timeout=DEFAULT)
        self.safe_fill(confirm_input, "DELETE")
        logger.info("[RestrictionsPage] DELETE confirmation entered")

        confirm_button = dialog.get_by_role("button", name="Delete")
        expect(confirm_button).to_be_enabled(timeout=DEFAULT)
        self.safe_click(confirm_button)
        logger.info("[RestrictionsPage] Delete confirmed")

    def close_popup(self) -> None:
        self._close_summary_popup()

    # =========================================================================
    # TC_09_01 — WORKFLOW DELETE RESTRICTION
    # =========================================================================

    def attempt_delete_workflow(self, workflow_name: str) -> None:
        self._row(workflow_name).get_by_role("checkbox").check()
        logger.info(f"[RestrictionsPage] Workflow selected: {workflow_name}")
        self.perform_delete_confirmation()

    # =========================================================================
    # TC_09_02 — TEMPLATE DELETE RESTRICTION
    # =========================================================================

    def attempt_delete_template(self, template_name: str) -> None:
        self._row(template_name).get_by_role("checkbox").check()
        logger.info(f"[RestrictionsPage] Template selected: {template_name}")
        self.perform_delete_confirmation()

    # =========================================================================
    # TC_09_03 — DATASET DELETE RESTRICTION
    # =========================================================================

    def attempt_delete_dataset(self, dataset_name: str) -> None:
        self._row(dataset_name).get_by_role("checkbox").check()
        logger.info(f"[RestrictionsPage] Dataset selected: {dataset_name}")
        self.perform_delete_confirmation()

    # =========================================================================
    # TC_09_04 — DATASET FILE DELETE RESTRICTION
    # =========================================================================

    def attempt_delete_dataset_files(self, file_names: list) -> None:
        for file_name in file_names:
            self._row(file_name).get_by_role("checkbox").check()
            logger.info(f"[RestrictionsPage] Dataset file selected: {file_name}")
        self.perform_delete_confirmation()

    # =========================================================================
    # TC_09_05 — FILES PAGE DELETE RESTRICTION
    # =========================================================================

    def attempt_delete_files(self, file_names: list) -> None:
        for file_name in file_names:
            self._row(file_name).get_by_role("checkbox").check()
            logger.info(f"[RestrictionsPage] File selected: {file_name}")
        self.perform_delete_confirmation()

    # =========================================================================
    # TC_09_06 — INTEGRATION DELETE RESTRICTION
    # =========================================================================

    def attempt_delete_integration(self, integration_name: str) -> None:
        self._row(integration_name).get_by_role("checkbox").check()
        logger.info(f"[RestrictionsPage] Integration selected: {integration_name}")
        self.perform_delete_confirmation()