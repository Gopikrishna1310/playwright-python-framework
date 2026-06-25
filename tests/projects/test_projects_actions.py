import re
import logging
import pytest

from utils.waits import LOAD

from pages.common.login_page import LoginPage
from pages.common.sidebar_page import SidebarPage
from pages.projects.projects_page import ProjectsPage
from config.credentials import TOOL_EMAIL, TOOL_PASSWORD

logger = logging.getLogger(__name__)


@pytest.mark.projects
def test_projects_actions(page):

    # =========================================================================
    # LOGIN
    # =========================================================================

    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(TOOL_EMAIL, TOOL_PASSWORD)

    sidebar_page = SidebarPage(page)
    sidebar_page.select_organization_and_role()

    # =========================================================================
    # TC_08_01: Open Projects page
    # =========================================================================

    projects_page = ProjectsPage(page)

    # When: Click Projects from sidebar
    projects_page.open_projects_page()

    # Then: Projects list page should open
    projects_page.verify_projects_page_opened()
    logger.info("TC_08_01 Projects page opened and verified")

    # =========================================================================
    # TC_08_02: Create Project 1
    # =========================================================================

    # When: Click Create Project and fill details
    # Popup open is verified inside create_project() via heading visibility
    projects_page.create_project(
        project_name="Test project 1",
        datasets=["Test 3"],
        workflow="Testing workflow 1",
        description="Description"
    )

    # Then: Project should appear in the list
    projects_page.verify_project_in_list("Test project 1")
    logger.info("TC_08_02 Project 1 created and verified in list")

    # =========================================================================
    # TC_08_02: Create Project 2
    # =========================================================================

    projects_page.create_project(
        project_name="Test project 2",
        datasets=["Test audio 2"],
        workflow="Testing workflow 1"
    )

    projects_page.verify_project_in_list("Test project 2")
    logger.info("TC_08_02 Project 2 created and verified in list")

    # =========================================================================
    # TC_08_03: Delete Project 2
    # =========================================================================

    # When: Select project checkbox
    projects_page._project_row("Test project 2").get_by_role("checkbox").check()

    # Then: Delete button should be enabled
    projects_page.verify_delete_button_enabled()

    # When: Click Delete and confirm
    projects_page.safe_click(page.get_by_role("button", name="Delete"))
    dialog = projects_page._dialog()
    projects_page.safe_fill(dialog.get_by_role("textbox"), "DELETE")
    projects_page.safe_click(dialog.get_by_role("button", name="Delete"))
    projects_page._close_summary_popup()

    # Reload before verifying — same fix as datasets/users:
    # delete may update the DOM optimistically before the backend
    # actually removes the row. Reload forces a real server fetch.
    page.reload()
    projects_page.wait.for_url_contains("/projects", timeout=LOAD)

    # Then: Deleted project should not be in the list
    projects_page.verify_project_not_in_list("Test project 2")
    logger.info("TC_08_03 Project 2 deleted and verified not in list")

    # =========================================================================
    # TC_08_04: Tasks page
    # =========================================================================

    # When: Click project
    projects_page.open_project("Test project 1")

    # Then: Tasks tab should be open by default
    projects_page.verify_tasks_tab_open()
    logger.info("TC_08_04 Tasks tab verified")

    # =========================================================================
    # TC_08_05: Export
    # =========================================================================

    # When: Click Export
    projects_page.export_project_data()
    logger.info("TC_08_05 Export completed")

    # =========================================================================
    # TC_08_06: Reset tasks
    # =========================================================================

    # When: Select a task
    task_row = page.get_by_role("row", name=re.compile(r"audio 4\.wav"))
    task_row.get_by_role("checkbox").check()

    # Then: Reset button should be enabled
    projects_page.verify_reset_button_enabled()

    # When: Reset the task
    projects_page.reset_tasks(["audio 4.wav"])
    logger.info("TC_08_06 Reset tasks completed")

    # =========================================================================
    # TC_08_07: Add dataset
    # =========================================================================

    # When: Click Datasets tab
    page.get_by_role("tab", name="Datasets").click()

    # Then: Datasets tab should open
    projects_page.verify_datasets_tab_open()

    # When: Click Add and select dataset
    page.get_by_role("button", name="Add").click()
    dataset_row = page.get_by_role("row", name=re.compile(r"Test audio 2"))
    dataset_row.get_by_role("checkbox").check()

    # Then: Add/Sync button should be enabled
    projects_page.verify_add_sync_button_enabled()

    # When: Click Add/Sync
    page.get_by_role("button", name="Add/Sync").click()

    # Then: Dataset should appear in project datasets list
    projects_page.verify_dataset_in_project("Test audio 2")
    logger.info("TC_08_07 Dataset added and verified in project")

    # =========================================================================
    # TC_08_08: Add annotators
    # =========================================================================

    projects_page.add_project_users(
        role="ANNOTATOR",
        users=["Objectways Annotator 1", "Objectways Annotator 2"]
    )

    # Then: Annotators should be visible in Teams tab
    projects_page.verify_user_in_teams("Objectways Annotator 1")
    projects_page.verify_user_in_teams("Objectways Annotator 2")
    logger.info("TC_08_08 Annotators added and verified in Teams")

    # =========================================================================
    # TC_08_09: Add reviewer
    # =========================================================================

    projects_page.add_project_users(
        role="REVIEWER",
        users=["Objectways Reviewer"]
    )

    # Then: Reviewer should be visible in Teams tab
    projects_page.verify_user_in_teams("Objectways Reviewer")
    logger.info("TC_08_09 Reviewer added and verified in Teams")

    # =========================================================================
    # TC_08_10: Remove user
    # =========================================================================

    # When: Select Annotator 2
    page.get_by_role("tab", name="Teams").click()
    annotator2_row = page.get_by_role(
        "row", name=re.compile(r"Objectways Annotator 2")
    )
    annotator2_row.get_by_role("checkbox").check()

    # Then: Remove Selected button should be enabled
    projects_page.verify_remove_selected_enabled()

    # When: Click Remove Selected
    page.get_by_role("button", name=re.compile(r"Remove Selected")).click()

    # Then: Confirmation popup should open
    projects_page.verify_remove_confirmation_popup_open()

    # When: Type DELETE in confirmation field
    dialog = projects_page._dialog()
    projects_page.safe_fill(dialog.get_by_role("textbox"), "DELETE")

    # Then: Remove button should be enabled
    projects_page.verify_remove_button_enabled_in_dialog()

    # When: Click Remove
    projects_page.safe_click(dialog.get_by_role("button", name="Remove"))

    # Then: User should not be in the list
    projects_page.verify_user_not_in_teams("Objectways Annotator 2")
    logger.info("TC_08_10 Annotator 2 removed and verified not in Teams")

    logger.info("Projects regression completed successfully")