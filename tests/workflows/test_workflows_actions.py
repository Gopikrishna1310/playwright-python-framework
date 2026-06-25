import logging
import pytest

from pages.common.login_page import LoginPage
from pages.workflows.workflows_page import WorkflowsPage
from config.credentials import TOOL_EMAIL, TOOL_PASSWORD

logger = logging.getLogger(__name__)


@pytest.mark.workflows
def test_create_workflows(page):

    # =========================================================================
    # LOGIN
    # =========================================================================

    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(TOOL_EMAIL, TOOL_PASSWORD)

    # =========================================================================
    # TC_06_01: Open Workflows page
    # =========================================================================

    workflow = WorkflowsPage(page)

    # When: Click Workflows from sidebar
    workflow.open_workflows_page()

    # Then: Workflows list page should open
    workflow.verify_workflows_page_opened()
    logger.info("TC_06_01 Workflows page opened and verified")

    # =========================================================================
    # TC_06_02 + TC_06_03: Create Workflow 1
    # =========================================================================

    # When: Click Create Workflow, fill name and description
    workflow.create_workflow("Testing workflow 1", "Description")

    # When: Click Start node
    workflow.create_nodes()

    # Then: Annotate node should be on canvas
    workflow.verify_node_on_canvas(".react-flow__node-annotate", "Annotate")

    # When: Click + on Annotate node
    workflow.select_template()

    # Then: Template should be visible in the menu
    # (already verified inside select_template via wait — explicit log confirms)
    logger.info("TC_06_03 Template 'Test template - 1' visible after clicking +")

    # When: Connect Reject -> Annotate
    workflow.connect_reject_to_annotate()

    # Then: Edge should be connected
    workflow.verify_edge_connected()
    logger.info("TC_06_02 Reject connected to Annotate — edge verified")

    # When: Save workflow
    workflow.save_workflow()

    # Return to list
    workflow.open_workflows_page()

    # Then: Workflow 1 should appear in the list
    workflow.verify_workflow_visible("Testing workflow 1")
    logger.info("TC_06_02 Workflow 1 created and verified in list")

    # =========================================================================
    # TC_06_02 + TC_06_03: Create Workflow 2
    # =========================================================================

    workflow.create_workflow("Testing workflow 2")
    workflow.create_nodes()

    # Then: Annotate node should be on canvas
    workflow.verify_node_on_canvas(".react-flow__node-annotate", "Annotate")

    workflow.select_template()
    logger.info("TC_06_03 Template visible for Workflow 2")

    workflow.connect_reject_to_annotate()
    workflow.verify_edge_connected()
    logger.info("TC_06_02 Reject connected to Annotate for Workflow 2")

    workflow.save_workflow()

    workflow.open_workflows_page()

    # Then: Workflow 2 should appear in the list
    workflow.verify_workflow_visible("Testing workflow 2")
    logger.info("TC_06_02 Workflow 2 created and verified in list")

    # =========================================================================
    # TC_06_04: Delete Workflow 2
    # =========================================================================

    # When: Select and delete workflow
    workflow.delete_workflow("Testing workflow 2")

    # Then: Deleted workflow should not be visible
    workflow.verify_workflow_not_visible("Testing workflow 2")
    logger.info("TC_06_04 Workflow 2 deleted and verified not visible")

    logger.info("All workflow automation completed successfully")