from pathlib import Path
from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils

class WorkflowsActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)

    def click_workflows_menu(self):
        self.ui_utils.click_element(self.page_factory.workflows_page.workflows_menu)
        self.ui_utils.element_wait_for(self.page_factory.workflows_page.create_workflow_btn, state="visible", timeout=10000)
        create_workflow_btn_visible = self.ui_utils.is_element_visible(self.page_factory.workflows_page.create_workflow_btn, timeout=10000)
        print(f"Create Workflow button visibility: {create_workflow_btn_visible}")
        if create_workflow_btn_visible:
            print("Create Workflow button is visible")
        else:
            raise Exception("Create Workflow button is not visible after clicking the Workflows menu.")

    def create_workflow(self, workflow_name, description=None):
        self.ui_utils.click_element(self.page_factory.workflows_page.create_workflow_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.fill_input(self.page_factory.workflows_page.enter_workflow_name_input, workflow_name)
        if description:
            self.ui_utils.fill_input(self.page_factory.workflows_page.description_input, description)
        self.ui_utils.click_element(self.page_factory.workflows_page.next_button)
        self.ui_utils.element_wait_for(self.page_factory.workflows_page.workflow_chart, state="visible", timeout=10000)
        workflow_chart_visible = self.ui_utils.is_element_visible(self.page_factory.workflows_page.workflow_chart, timeout=10000)
        print(f"Workflow chart visibility: {workflow_chart_visible}")
        if workflow_chart_visible:
            print("Workflow chart is visible")
        else:
            raise Exception("Workflow chart is not visible after creating the workflow.")

    def click_nodes(self, node_name):
        node_locator = self.page_factory.workflows_page.click_nodes_workflow(node_name)
        self.ui_utils.click_element(node_locator)
        self.ui_utils.element_wait_for(self.page_factory.workflows_page.verify_nodes_in_workflow_chart(node_name), state="visible", timeout=10000)
        node_visible = self.ui_utils.is_element_visible(self.page_factory.workflows_page.verify_nodes_in_workflow_chart(node_name))
        if node_visible:
            print(f"Node '{node_name}' is visible in the workflow chart")
        else:
            raise Exception(f"Node '{node_name}' is not visible in the workflow chart after clicking it.")

    def apply_template_to_annotate(self, template_name, position=0):
        self.ui_utils.click_element(self.page_factory.workflows_page.plus_icon.nth(position))
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.workflows_page.get_template_option(template_name))

    def nodes_connection_flow(self, node_Name1, position1 , index1, node_Name2, position2, index2):
        source = self.page_factory.workflows_page.get_node_connector(node_Name1, position1, index1)
        target = self.page_factory.workflows_page.get_node_connector(node_Name2, position2,  index2)
        self.ui_utils.drag_and_drop(source, target)
        

