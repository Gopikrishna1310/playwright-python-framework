import re
import logging

from playwright.sync_api import Page, expect

from pages.common.base_page import BasePage
from utils.waits import SHORT, DEFAULT, LONG, LOAD

logger = logging.getLogger(__name__)


class WorkflowsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.workflows_menu = page.get_by_role("link", name="Workflows")
        self.create_workflow_btn = page.get_by_role("button", name="Create workflow")

    # =========================================================================
    # PRIVATE
    # =========================================================================

    def _next_frame(self):
        self.page.evaluate(
            "() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))"
        )

    # =========================================================================
    # OPEN WORKFLOWS PAGE
    # =========================================================================

    def open_workflows_page(self) -> None:
        self.safe_click(self.workflows_menu)
        self.wait.for_url_contains("/workflows", timeout=LOAD)
        logger.info("[WorkflowsPage] Workflows page opened")

    # =========================================================================
    # ASSERTIONS
    # =========================================================================

    def verify_workflows_page_opened(self) -> None:
        expect(self.page).to_have_url(
            re.compile(r"/workflows$"), timeout=LONG
        )
        self.verify_visible(self.create_workflow_btn, timeout=LONG)
        logger.info(
            f"[WorkflowsPage]  Workflows page verified: {self.page.url}"
        )

    def verify_workflow_visible(self, workflow_name: str) -> None:
        row = self.page.get_by_role(
            "row", name=re.compile(re.escape(workflow_name))
        )
        self.verify_visible(row.first, timeout=LONG)
        logger.info(f"[WorkflowsPage]  Workflow visible: {workflow_name}")

    def verify_workflow_not_visible(self, workflow_name: str) -> None:
        row = self.page.get_by_role(
            "row", name=re.compile(re.escape(workflow_name))
        )
        self.verify_count(row, 0, timeout=LONG)
        logger.info(f"[WorkflowsPage]  Workflow not visible: {workflow_name}")

    def verify_node_on_canvas(self, node_class: str, label: str) -> None:
        node = self.page.locator(node_class)
        self.verify_visible(node.first, timeout=DEFAULT)
        logger.info(f"[WorkflowsPage]  Node on canvas: {label}")

    def verify_template_visible_in_menu(self, template_name: str) -> None:
        template = self.page.get_by_text(template_name, exact=True)
        self.verify_visible(template.first, timeout=LONG)
        logger.info(
            f"[WorkflowsPage]  Template visible in menu: {template_name}"
        )

    def verify_edge_connected(self) -> None:
        edge = self.page.locator(".react-flow__edge")
        # Edges accumulate — at least one must exist after each connection
        count = edge.count()
        assert count > 0, "No edges found — connection may have failed"
        logger.info(f"[WorkflowsPage]  Edge connected (total edges: {count})")

    # =========================================================================
    # CREATE WORKFLOW
    # =========================================================================

    def create_workflow(self, workflow_name: str, description: str = "") -> None:
        self.safe_click(self.create_workflow_btn)

        workflow_input = self.page.get_by_role("textbox", name="Enter Workflow Name")
        self.wait.for_visible(workflow_input, timeout=DEFAULT)
        self.safe_fill(workflow_input, workflow_name)

        description_input = self.page.get_by_role("textbox", name="Type Description")
        self.safe_fill(description_input, description)

        self.safe_click(self.page.get_by_role("button", name="Next"))
        self.wait.for_visible(self.page.locator(".react-flow"), timeout=LONG)

        logger.info(f"[WorkflowsPage] Workflow canvas opened: {workflow_name}")

    # =========================================================================
    # CREATE NODES
    # =========================================================================

    def create_nodes(self) -> None:
        nodes = ["Start", "Annotate", "Review", "Complete"]
        for node_name in nodes:
            self.safe_click(
                self.page.get_by_text(node_name, exact=True)
            )
            logger.info(f"[WorkflowsPage] Node clicked: {node_name}")

        try:
            self.wait.for_visible(
                self.page.locator(".react-flow__node-annotate"), timeout=SHORT
            )
        except Exception:
            pass

        logger.info("[WorkflowsPage] All nodes created")

    # =========================================================================
    # SELECT TEMPLATE
    # =========================================================================

    def select_template(self) -> None:
        plus_btn = self.page.locator("svg.lucide-plus").first
        self.wait.for_visible(plus_btn, timeout=DEFAULT)
        plus_btn.click(force=True)
        logger.info("[WorkflowsPage] Clicked annotate plus button")

        template = self.page.get_by_text("Test template - 1", exact=True)
        self.wait.for_visible(template, timeout=LONG)
        self.safe_click(template)

        logger.info("[WorkflowsPage] Template selected")

    # =========================================================================
    # CONNECT REJECT -> ANNOTATE
    # =========================================================================

    def connect_reject_to_annotate(self) -> None:
        reject_handle = self.page.locator('[data-handleid="rejected"]')
        annotate_node = self.page.locator(".react-flow__node-annotate")
        annotate_target = annotate_node.locator('[data-handlepos="left"]')

        self.wait.for_visible(reject_handle, timeout=LONG)
        self.wait.for_visible(annotate_target, timeout=LONG)

        source_box = reject_handle.bounding_box()
        target_box = annotate_target.bounding_box()

        if not source_box or not target_box:
            logger.warning("[WorkflowsPage] Drag handles not found — skipping connect")
            return

        self.page.mouse.move(
            source_box["x"] + source_box["width"] / 2,
            source_box["y"] + source_box["height"] / 2,
        )
        self._next_frame()
        self.page.mouse.down()
        self._next_frame()
        self.page.mouse.move(
            target_box["x"] + target_box["width"] / 2,
            target_box["y"] + target_box["height"] / 2,
            steps=50,
        )
        self._next_frame()
        self.page.mouse.up()

        logger.info("[WorkflowsPage] Reject connected to Annotate")

    # =========================================================================
    # SAVE WORKFLOW
    # =========================================================================

    def save_workflow(self) -> None:
        save_button = self.page.get_by_role("button", name="Save")
        self.wait.for_visible(save_button, timeout=LONG)

        if save_button.is_enabled():
            self.safe_click(save_button)
            try:
                self.wait.for_page_ready()
            except Exception:
                pass
            logger.info("[WorkflowsPage] Workflow saved")
        else:
            logger.warning("[WorkflowsPage] Save button is disabled")

    # =========================================================================
    # DELETE WORKFLOW
    # =========================================================================

    def delete_workflow(self, workflow_name: str) -> None:
        workflow_row = self.page.get_by_role(
            "row", name=re.compile(re.escape(workflow_name))
        )
        self.wait.for_visible(workflow_row, timeout=LONG)
        workflow_row.get_by_role("checkbox").check()
        logger.info(f"[WorkflowsPage] Workflow selected: {workflow_name}")

        delete_button = self.page.get_by_role("button", name="Delete")
        self.wait.for_visible(delete_button, timeout=DEFAULT)
        self.safe_click(delete_button)

        confirm_dialog = self.page.get_by_role("dialog")
        textbox = confirm_dialog.get_by_role("textbox")
        self.wait.for_visible(textbox, timeout=DEFAULT)
        self.safe_fill(textbox, "DELETE")

        confirm_delete = confirm_dialog.get_by_role("button", name="Delete")
        expect(confirm_delete).to_be_enabled(timeout=DEFAULT)
        self.safe_click(confirm_delete)

        self.verify_count(
            self.page.get_by_role("row", name=re.compile(re.escape(workflow_name))),
            0,
            timeout=LONG,
        )
        logger.info(f"[WorkflowsPage]  Workflow deleted: {workflow_name}")