import pytest

from pages.common.login_page import LoginPage
from pages.common.sidebar_page import SidebarPage

from pages.projects.projects_page import ProjectsPage

from config.credentials import (
    TOOL_EMAIL,
    TOOL_PASSWORD
)


@pytest.mark.projects
def test_projects_actions(page):

    # ============================================
    # LOGIN
    # ============================================

    login_page = LoginPage(page)

    login_page.open_login_page()

    login_page.login(
        TOOL_EMAIL,
        TOOL_PASSWORD
    )

    # ============================================
    # ORGANIZATION + ROLE
    # ============================================

    sidebar_page = SidebarPage(page)

    sidebar_page.select_organization_and_role()

    print(
        "\nLogin successful"
    )

    # ============================================
    # OPEN PROJECTS PAGE
    # ============================================

    projects_page = ProjectsPage(page)

    projects_page.open_projects_page()

    projects_page.validate_projects_page_opened()

    print(
        "\nTC_08_01 Open Projects page completed"
    )

    # ============================================
    # TC_08_02
    # CREATE PROJECT 1
    # ============================================

    projects_page.create_project(
        project_name="Test project 1",
        datasets=[
            "Test 3"
        ],
        workflow="Testing workflow 1",
        description="Description"
    )

    print(
        "\nTC_08_02 Project 1 creation completed"
    )

    # ============================================
    # CREATE PROJECT 2
    # ============================================

    projects_page.create_project(
        project_name="Test project 2",
        datasets=[
            "Test audio 2"
        ],
        workflow="Testing workflow 1"
    )

    print(
        "\nTC_08_02 Project 2 creation completed"
    )

    # ============================================
    # TC_08_03
    # DELETE PROJECT 2
    # ============================================

    projects_page.delete_project(
        "Test project 2"
    )

    print(
        "\nTC_08_03 Delete Project completed"
    )

    # ============================================
    # OPEN PROJECT 1
    # ============================================

    projects_page.open_project(
        "Test project 1"
    )

    # ============================================
    # TC_08_04
    # TASKS PAGE VALIDATION
    # ============================================

    projects_page.validate_tasks_page()

    print(
        "\nTC_08_04 Tasks page validation completed"
    )

    # ============================================
    # TC_08_05
    # EXPORT PROJECT DATA
    # ============================================

    projects_page.export_project_data()

    print(
        "\nTC_08_05 Export completed"
    )

    # ============================================
    # TC_08_06
    # RESET TASKS
    # ============================================

    projects_page.reset_tasks(
        [
            "audio 4.wav"
        ]
    )

    print(
        "\nTC_08_06 Reset tasks completed"
    )

    # ============================================
    # TC_08_07
    # ADD DATASET TO PROJECT
    # ============================================

    projects_page.add_dataset_to_project(
        "Test audio 2"
    )

    print(
        "\nTC_08_07 Add dataset completed"
    )

    # ============================================
    # TC_08_08
    # ADD ANNOTATORS
    # ============================================

    projects_page.add_project_users(
        role="ANNOTATOR",
        users=[
            "Objectways Annotator 1",
            "Objectways Annotator 2"
        ]
    )

    print(
        "\nTC_08_08 Add annotators completed"
    )

    # ============================================
    # TC_08_09
    # ADD REVIEWERS
    # ============================================

    projects_page.add_project_users(
        role="REVIEWER",
        users=[
            "Objectways Reviewer"
        ]
    )

    print(
        "\nTC_08_09 Add reviewers completed"
    )

    # ============================================
    # TC_08_10
    # REMOVE USERS
    # ============================================

    projects_page.remove_project_users(
        [
            "Objectways Annotator 2"
        ]
    )

    print(
        "\nTC_08_10 Remove users completed"
    )