import re
import logging

from playwright.sync_api import expect, Page

from pages.common.base_page import BasePage
from utils.waits import SHORT, DEFAULT, LONG, LOAD

logger = logging.getLogger(__name__)


class ProjectsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.projects_menu         = page.get_by_role("link", name="Projects")
        self.create_project_btn    = page.get_by_role("button", name="Create Project")
        self.delete_toolbar_btn    = page.get_by_role("button", name="Delete")
        self.projects_heading      = page.get_by_role("heading", name="Projects")
        self.create_project_heading = page.get_by_role("heading", name="Create Project")

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
                    logger.info("[ProjectsPage] Summary popup closed")
                    return
            except Exception:
                continue
        logger.info("[ProjectsPage] No summary popup to close")

    def _project_row(self, project_name: str):
        return self.page.get_by_role(
            "row", name=re.compile(re.escape(project_name))
        )

    # =========================================================================
    # OPEN PROJECTS PAGE
    # =========================================================================

    def open_projects_page(self) -> None:
        self.safe_click(self.projects_menu)
        self.wait.for_url_contains("/projects", timeout=LOAD)
        logger.info("[ProjectsPage] Projects page opened")

    # =========================================================================
    # ASSERTIONS
    # =========================================================================

    def verify_projects_page_opened(self) -> None:
        expect(self.page).to_have_url(
            re.compile(r"/projects$"), timeout=LONG
        )
        self.verify_visible(self.projects_heading, timeout=LONG)
        logger.info(
            f"[ProjectsPage]  Projects page verified: {self.page.url}"
        )

    def verify_create_project_popup_opened(self) -> None:
        self.verify_visible(self.create_project_heading, timeout=DEFAULT)
        logger.info("[ProjectsPage]  Create Project popup is open")

    def verify_create_project_button_enabled(self) -> None:
        dialog = self._dialog()
        btn = dialog.get_by_role("button", name="Create Project")
        self.verify_enabled(btn, timeout=DEFAULT)
        logger.info("[ProjectsPage]  Create Project button is enabled")

    def verify_project_in_list(self, project_name: str) -> None:
        self.verify_visible(
            self._project_row(project_name).first, timeout=LONG
        )
        logger.info(f"[ProjectsPage]  Project visible in list: {project_name}")

    def verify_project_not_in_list(self, project_name: str) -> None:
        self.verify_count(self._project_row(project_name), 0, timeout=LONG)
        logger.info(
            f"[ProjectsPage]  Project not visible in list: {project_name}"
        )

    def verify_delete_button_enabled(self) -> None:
        self.verify_enabled(self.delete_toolbar_btn, timeout=DEFAULT)
        logger.info("[ProjectsPage]  Delete button is enabled")

    def verify_tasks_tab_open(self) -> None:
        self.verify_visible(
            self.page.get_by_role("button", name="Export"), timeout=LONG
        )
        self.verify_visible(
            self.page.get_by_role("button", name="Reset"), timeout=LONG
        )
        self.verify_visible(
            self.page.get_by_role("textbox", name="search").first, timeout=LONG
        )
        logger.info("[ProjectsPage]  Tasks tab verified (Export, Reset, Search visible)")

    def verify_reset_button_enabled(self) -> None:
        self.verify_enabled(
            self.page.get_by_role("button", name="Reset"), timeout=DEFAULT
        )
        logger.info("[ProjectsPage]  Reset button is enabled")

    def verify_datasets_tab_open(self) -> None:
        self.verify_visible(
            self.page.get_by_role("button", name="Add"), timeout=LONG
        )
        logger.info("[ProjectsPage]  Datasets tab opened")

    def verify_add_sync_button_enabled(self) -> None:
        self.verify_enabled(
            self.page.get_by_role("button", name="Add/Sync"), timeout=DEFAULT
        )
        logger.info("[ProjectsPage]  Add/Sync button is enabled")

    def verify_dataset_in_project(self, dataset_name: str) -> None:
        self.verify_visible(
            self.page.get_by_role(
                "row", name=re.compile(re.escape(dataset_name))
            ).first,
            timeout=LONG
        )
        logger.info(f"[ProjectsPage]  Dataset visible in project: {dataset_name}")

    def verify_user_in_teams(self, user_name: str) -> None:
        self.verify_visible(
            self.page.get_by_role(
                "row", name=re.compile(re.escape(user_name))
            ).first,
            timeout=LONG
        )
        logger.info(f"[ProjectsPage]  User visible in Teams: {user_name}")

    def verify_user_not_in_teams(self, user_name: str) -> None:
        self.verify_count(
            self.page.get_by_role(
                "row", name=re.compile(re.escape(user_name))
            ),
            0,
            timeout=LONG
        )
        logger.info(f"[ProjectsPage]  User not in Teams: {user_name}")

    def verify_remove_selected_enabled(self) -> None:
        self.verify_enabled(
            self.page.get_by_role(
                "button", name=re.compile(r"Remove Selected")
            ),
            timeout=DEFAULT
        )
        logger.info("[ProjectsPage]  Remove Selected button is enabled")

    def verify_remove_confirmation_popup_open(self) -> None:
        self.verify_visible(
            self.page.get_by_role(
                "heading", name="Remove Users Confirmation"
            ),
            timeout=DEFAULT
        )
        logger.info("[ProjectsPage]  Remove Users Confirmation popup is open")

    def verify_remove_button_enabled_in_dialog(self) -> None:
        dialog = self._dialog()
        self.verify_enabled(
            dialog.get_by_role("button", name="Remove"),
            timeout=DEFAULT
        )
        logger.info("[ProjectsPage]  Remove button enabled in confirmation popup")

    # =========================================================================
    # CREATE PROJECT
    # =========================================================================

    def create_project(
        self,
        project_name: str,
        datasets: list,
        workflow: str,
        description: str = ""
    ) -> None:
        self.safe_click(self.create_project_btn)

        name_input = self.page.get_by_role("textbox", name="Enter Project Name")
        self.wait.for_visible(name_input, timeout=DEFAULT)
        self.verify_visible(self.create_project_heading, timeout=DEFAULT)
        logger.info("[ProjectsPage]  Create Project popup opened")

        self.safe_fill(name_input, project_name)
        logger.info(f"[ProjectsPage] Project name entered: {project_name}")

        self.safe_click(self.page.get_by_role("button", name="Select Datasets"))
        first_ds = self.page.locator("div").filter(
            has_text=re.compile(rf"^{re.escape(datasets[0])}$")
        )
        self.wait.for_visible(first_ds, timeout=DEFAULT)

        for dataset_name in datasets:
            ds_locator = self.page.locator("div").filter(
                has_text=re.compile(rf"^{re.escape(dataset_name)}$")
            )
            self.safe_check(ds_locator.locator("input[type='checkbox']"))
            logger.info(f"[ProjectsPage] Dataset selected: {dataset_name}")

        self.safe_click(
            self.page.get_by_role(
                "button", name=re.compile(r"dataset\(s\) selected")
            )
        )

        self.safe_click(self.page.get_by_role("button", name="Select Workflow"))
        workflow_option = self.page.locator("div").filter(
            has_text=re.compile(rf"^{re.escape(workflow)}$")
        )
        self.wait.for_visible(workflow_option, timeout=DEFAULT)
        self.safe_click(workflow_option)
        logger.info(f"[ProjectsPage] Workflow selected: {workflow}")

        if description:
            self.safe_fill(
                self.page.get_by_role(
                    "textbox", name="Enter Project Description"
                ),
                description,
            )

        # Scope to dialog — toolbar "Create Project" is disabled when popup
        # is open and would cause a 30s timeout if matched instead
        dialog_submit = self.page.get_by_role("dialog").get_by_role(
            "button", name="Create Project"
        )
        self.safe_click(dialog_submit)
        logger.info("[ProjectsPage] Create Project submitted")

        expect(
            self._project_row(project_name).first
        ).to_be_visible(timeout=LONG)
        logger.info(f"[ProjectsPage] Project created: {project_name}")

    # =========================================================================
    # DELETE PROJECT
    # =========================================================================

    def delete_project(self, project_name: str) -> None:
        self._project_row(project_name).get_by_role("checkbox").check()
        logger.info(f"[ProjectsPage] Project selected: {project_name}")

        self.safe_click(self.page.get_by_role("button", name="Delete"))

        dialog = self._dialog()
        confirm_input = dialog.get_by_role("textbox")
        self.wait.for_visible(confirm_input, timeout=DEFAULT)
        self.safe_fill(confirm_input, "DELETE")

        self.safe_click(dialog.get_by_role("button", name="Delete"))
        logger.info(f"[ProjectsPage] Delete confirmed: {project_name}")

        self.verify_count(self._project_row(project_name), 0, timeout=LONG)
        self._close_summary_popup()

    # =========================================================================
    # OPEN PROJECT
    # =========================================================================

    def open_project(self, project_name: str) -> None:
        self.safe_click(self.page.get_by_text(project_name, exact=True))
        logger.info(f"[ProjectsPage] Project opened: {project_name}")

    # =========================================================================
    # TASKS
    # =========================================================================

    def validate_tasks_page(self) -> None:
        expect(
            self.page.get_by_role("button", name="Export")
        ).to_be_visible(timeout=LONG)
        expect(
            self.page.get_by_role("button", name="Reset")
        ).to_be_visible(timeout=LONG)
        expect(
            self.page.get_by_role("textbox", name="search").first
        ).to_be_visible(timeout=LONG)
        logger.info("[ProjectsPage] Tasks page controls validated")

    def export_project_data(self) -> None:
        with self.page.expect_download(timeout=LONG):
            self.safe_click(self.page.get_by_role("button", name="Export"))
        logger.info("[ProjectsPage] Export completed")

    def reset_tasks(self, file_names: list) -> None:
        for file_name in file_names:
            row = self.page.get_by_role(
                "row", name=re.compile(re.escape(file_name))
            )
            self.safe_check(row.get_by_role("checkbox"))
            logger.info(f"[ProjectsPage] Task selected: {file_name}")

        self.safe_click(self.page.get_by_role("button", name="Reset"))

        dialog = self._dialog()
        confirm_input = dialog.get_by_role("textbox")
        self.wait.for_visible(confirm_input, timeout=DEFAULT)
        self.safe_fill(confirm_input, "RESET")

        confirm_button = dialog.get_by_role("button", name="Reset")
        expect(confirm_button).to_be_enabled(timeout=DEFAULT)
        self.safe_click(confirm_button)
        self._close_summary_popup()
        logger.info("[ProjectsPage] Tasks reset completed")

    # =========================================================================
    # DATASETS TAB
    # =========================================================================

    def add_dataset_to_project(self, dataset_name: str) -> None:
        self.safe_click(self.page.get_by_role("tab", name="Datasets"))
        self.safe_click(self.page.get_by_role("button", name="Add"))

        row = self.page.get_by_role(
            "row", name=re.compile(re.escape(dataset_name))
        )
        self.safe_check(row.get_by_role("checkbox"))
        logger.info(f"[ProjectsPage] Dataset selected in popup: {dataset_name}")

        self.safe_click(self.page.get_by_role("button", name="Add/Sync"))

        expect(
            self.page.get_by_role(
                "row", name=re.compile(re.escape(dataset_name))
            ).first
        ).to_be_visible(timeout=LONG)
        logger.info(f"[ProjectsPage] Dataset added to project: {dataset_name}")

    # =========================================================================
    # TEAMS TAB
    # =========================================================================

    def add_project_users(self, role: str, users: list) -> None:
        self.safe_click(self.page.get_by_role("tab", name="Teams"))
        self.safe_click(self.page.get_by_role("button", name="Add Users"))

        first_row = self.page.get_by_role(
            "row", name=re.compile(re.escape(users[0]))
        )
        self.wait.for_visible(first_row, timeout=DEFAULT)

        if role != "ANNOTATOR":
            self.safe_select(self.page.get_by_role("combobox"), role)

        for user in users:
            row = self.page.get_by_role(
                "row", name=re.compile(re.escape(user))
            )
            self.safe_check(row.get_by_role("checkbox"))
            logger.info(f"[ProjectsPage] User selected: {user}")

        self.safe_click(self.page.get_by_role("button", name="Add"))

        for user in users:
            expect(
                self.page.get_by_role(
                    "row", name=re.compile(re.escape(user))
                ).first
            ).to_be_visible(timeout=LONG)
            logger.info(f"[ProjectsPage] User added to project: {user}")

    def remove_project_users(self, users: list) -> None:
        self.safe_click(self.page.get_by_role("tab", name="Teams"))

        first_row = self.page.get_by_role(
            "row", name=re.compile(re.escape(users[0]))
        )
        self.wait.for_visible(first_row, timeout=DEFAULT)

        for user in users:
            row = self.page.get_by_role(
                "row", name=re.compile(re.escape(user))
            )
            self.safe_check(row.get_by_role("checkbox"))
            logger.info(f"[ProjectsPage] User selected for removal: {user}")

        remove_button = self.page.get_by_role(
            "button", name=re.compile(r"Remove Selected")
        )
        expect(remove_button).to_be_enabled(timeout=DEFAULT)
        self.safe_click(remove_button)

        dialog = self._dialog()
        confirm_input = dialog.get_by_role("textbox")
        self.wait.for_visible(confirm_input, timeout=DEFAULT)
        self.safe_fill(confirm_input, "DELETE")

        confirm_button = dialog.get_by_role("button", name="Remove")
        self.safe_click(confirm_button)

        for user in users:
            self.verify_count(
                self.page.get_by_role(
                    "row", name=re.compile(re.escape(user))
                ),
                0,
                timeout=LONG,
            )
            logger.info(f"[ProjectsPage]  User removed: {user}")