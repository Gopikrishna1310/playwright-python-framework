import pytest

from pages.common.login_page import LoginPage

from pages.workflows.workflows_page import WorkflowsPage

from config.credentials import (
    TOOL_EMAIL,
    TOOL_PASSWORD
)


@pytest.mark.workflows
def test_create_workflows(page):

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
    # WORKFLOW PAGE
    # ============================================

    workflow = WorkflowsPage(page)

    workflow.open_workflows_page()

    workflow.validate_workflows_page_opened()

    # ============================================
    # WORKFLOW 1
    # ============================================

    workflow.create_workflow(
        "Testing workflow 1",
        "Description"
    )

    workflow.create_nodes()

    workflow.select_template()

    workflow.connect_reject_to_annotate()

    workflow.save_workflow()

    print(
        "\nWorkflow 1 completed successfully"
    )

    # ============================================
    # RETURN TO WORKFLOWS PAGE
    # ============================================

    workflow.open_workflows_page()

    # ============================================
    # WORKFLOW 2
    # ============================================

    workflow.create_workflow(
        "Testing workflow 2"
    )

    workflow.create_nodes()

    workflow.select_template()

    workflow.connect_reject_to_annotate()

    workflow.save_workflow()

    print(
        "\nWorkflow 2 completed successfully"
    )

    # ============================================
    # RETURN TO WORKFLOWS PAGE
    # ============================================

    workflow.open_workflows_page()

    # ============================================
    # DELETE WORKFLOW 2
    # ============================================

    workflow.delete_workflow(
        "Testing workflow 2"
    )

    print(
        "\nWorkflow 2 deleted successfully"
    )

    # ============================================
    # FINAL MESSAGE
    # ============================================

    print(
        "\nAll workflow automation completed successfully"
    )