import re

from playwright.sync_api import Page

from pages.common.base_page import BasePage


class WorkflowsPage(BasePage):

    def __init__(
            self,
            page: Page
    ):

        super().__init__(page)

        self.workflows_menu = page.get_by_role(
            "link",
            name="Workflows"
        )

    # ============================================
    # OPEN WORKFLOWS PAGE
    # ============================================

    def open_workflows_page(self):

        self.safe_click(
            self.workflows_menu
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nWorkflows page opened"
        )

    # ============================================
    # VALIDATE WORKFLOWS PAGE
    # ============================================

    def validate_workflows_page_opened(self):

        self.page.wait_for_url(
            "**/workflows",
            timeout=60000
        )

        print(
            f"\nCurrent URL: {self.page.url}"
        )

        print(
            "\nWorkflows page validation successful"
        )

    # ============================================
    # CREATE WORKFLOW
    # ============================================

    def create_workflow(
            self,
            workflow_name,
            description=""
    ):

        create_button = self.page.get_by_role(
            "button",
            name="Create workflow"
        )

        self.safe_click(
            create_button
        )

        self.page.wait_for_timeout(1500)

        workflow_input = self.page.get_by_role(
            "textbox",
            name="Enter Workflow Name"
        )

        self.safe_fill(
            workflow_input,
            workflow_name
        )

        description_input = self.page.get_by_role(
            "textbox",
            name="Type Description"
        )

        self.safe_fill(
            description_input,
            description
        )

        next_button = self.page.get_by_role(
            "button",
            name="Next"
        )

        self.safe_click(
            next_button
        )

        # Canvas stabilization
        self.page.wait_for_timeout(4000)

        print(
            f"\nWorkflow '{workflow_name}' canvas opened"
        )

    # ============================================
    # CREATE NODES
    # ============================================

    def create_nodes(self):

        # Canvas rendering stabilization
        self.page.wait_for_timeout(3000)

        print(
            "\nStarting workflow automation"
        )

        nodes = [

            "Start",

            "Annotate",

            "Review",

            "Complete"
        ]

        for node_name in nodes:

            node = self.page.get_by_text(
                node_name,
                exact=True
            )

            self.safe_click(
                node
            )

            self.page.wait_for_timeout(1000)

        # Node propagation stabilization
        self.page.wait_for_timeout(3000)

        print(
            "\nNodes created"
        )

    # ============================================
    # SELECT TEMPLATE
    # ============================================

    def select_template(self):

        plus_btn = self.page.locator(
            'svg.lucide-plus'
        ).first

        plus_btn.wait_for(
            state="visible",
            timeout=30000
        )

        plus_btn.click(
            force=True
        )

        print(
            "\nClicked annotate plus button"
        )

        self.page.wait_for_timeout(1500)

        template = self.page.get_by_text(
            "Test template - 1",
            exact=True
        )

        self.safe_click(
            template
        )

        # Template rendering stabilization
        self.page.wait_for_timeout(3000)

        print(
            "\nTemplate selected"
        )

    # ============================================
    # CONNECT REJECT -> ANNOTATE
    # ============================================

    def connect_reject_to_annotate(self):

        reject_handle = self.page.locator(
            '[data-handleid="rejected"]'
        )

        annotate_node = self.page.locator(
            '.react-flow__node-annotate'
        )

        annotate_target = annotate_node.locator(
            '[data-handlepos="left"]'
        )

        reject_handle.wait_for(
            state="visible",
            timeout=30000
        )

        annotate_target.wait_for(
            state="visible",
            timeout=30000
        )

        source_box = reject_handle.bounding_box()

        target_box = annotate_target.bounding_box()

        # ============================================
        # SAFETY CHECK
        # ============================================

        if not source_box:

            print(
                "\nReject handle not found"
            )

            return

        if not target_box:

            print(
                "\nAnnotate target not found"
            )

            return

        print(
            "\nSource box:",
            source_box
        )

        print(
            "\nTarget box:",
            target_box
        )

        # ============================================
        # DRAG CONNECTION
        # ============================================

        self.page.mouse.move(
            source_box["x"] + source_box["width"] / 2,
            source_box["y"] + source_box["height"] / 2
        )

        self.page.wait_for_timeout(300)

        self.page.mouse.down()

        self.page.wait_for_timeout(300)

        self.page.mouse.move(
            target_box["x"] + target_box["width"] / 2,
            target_box["y"] + target_box["height"] / 2,
            steps=50
        )

        self.page.wait_for_timeout(300)

        self.page.mouse.up()

        # Connection propagation stabilization
        self.page.wait_for_timeout(3000)

        print(
            "\nReject connected to Annotate"
        )

    # ============================================
    # SAVE WORKFLOW
    # ============================================

    def save_workflow(self):

        save_button = self.page.get_by_role(
            "button",
            name="Save"
        )

        save_button.wait_for(
            state="visible",
            timeout=30000
        )

        if save_button.is_enabled():

            self.safe_click(
                save_button
            )

            # Save propagation stabilization
            self.page.wait_for_timeout(3000)

            print(
                "\nWorkflow saved successfully"
            )

        else:

            print(
                "\nSave button is disabled"
            )

    # ============================================
    # DELETE WORKFLOW
    # ============================================

    def delete_workflow(
            self,
            workflow_name
    ):

        workflow_row = self.page.get_by_role(
            "row",
            name=re.compile(workflow_name)
        )

        workflow_row.wait_for(
            state="visible",
            timeout=60000
        )

        workflow_row.get_by_role(
            "checkbox"
        ).check()

        print(
            f"\nSelected workflow:\n{workflow_name}"
        )

        self.page.wait_for_timeout(1000)

        delete_button = self.page.get_by_role(
            "button",
            name="Delete"
        )

        self.safe_click(
            delete_button
        )

        print(
            "\nClicked delete toolbar button"
        )

        self.page.wait_for_timeout(1500)

        confirm_dialog = self.page.get_by_role(
            "dialog"
        )

        textbox = confirm_dialog.get_by_role(
            "textbox"
        )

        self.safe_fill(
            textbox,
            "DELETE"
        )

        print(
            "\nEntered DELETE confirmation"
        )

        self.page.wait_for_timeout(1000)

        confirm_delete = confirm_dialog.get_by_role(
            "button",
            name="Delete"
        )

        self.safe_click(
            confirm_delete
        )

        # Backend delete propagation
        self.page.wait_for_timeout(3000)

        print(
            f"\nWorkflow '{workflow_name}' deleted successfully"
        )