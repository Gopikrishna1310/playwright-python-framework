from utils.ui_utils import UIUtils

class WorkflowsPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.frame = page.frame_locator("iframe")
        self.workflows_menu = page.get_by_role("link", name="Workflows")
        self.create_workflow_btn = page.get_by_role("button", name="Create workflow")
        self.enter_workflow_name_input = page.locator("input#workflowName")
        self.description_input = page.get_by_role('textbox', name= 'Description' )
        self.next_button = page.get_by_role('button', name= 'Next')
        self.workflow_chart = page.locator('.react-flow__pane')
        self.nodes_in_chart = page.locator("div[class*='node-start']")
        self.plus_icon = page.locator("svg[class*='lucide-plus']")
        self.template_name_list = page.locator("div[class*='medium cursor-pointer']")
        self.save_btn = page.get_by_role("button", name="Save")
        self.template_names_list = page.locator('div[class*="medium text"]')#changed
        self.fit_view = page.get_by_role('button', name= 'fit view')
        self.required_annotators = page.get_by_role('spinbutton', name= 'Required annotators' )

    def click_nodes_workflow(self, node_name):
        return self.page.locator(f"div[class*='space'] div[class*='{node_name.lower()}']")

    def verify_nodes_in_workflow_chart(self, nodesName):
        nodeNames = nodesName.strip().lower()
        return self.page.locator(f"div[class*='node-{nodeNames}']").first

    def get_template_option(self, template_name):
        return self.page.locator("span").filter(has_text=template_name)

    def get_node_connector(self, node_name: str, node_index: int, position: str, handle_index: int):
        nodes = self.page.locator(f"div[class*='node-{node_name}']")
        node = nodes.nth(node_index - 1)
        handle = node.locator(f"div[data-handlepos*='{position}']").nth(handle_index - 1)
        return handle
        

    

    