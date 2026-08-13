from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils

class ProjectsActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)

    def click_project_menu(self):
        self.ui_utils.click_element(self.page_factory.projects_page.project_menu)
        self.ui_utils.element_wait_for(self.page_factory.projects_page.create_project_btn, state="visible", timeout=10000)
        create_project_btn_visible = self.ui_utils.is_element_visible(self.page_factory.projects_page.create_project_btn, timeout=10000)
        print(f"Create Project button visibility: {create_project_btn_visible}")
        if create_project_btn_visible:
            print("Create Project button is visible")
        else:
            raise Exception("Create Project button is not visible after clicking the Projects menu.")

    def create_project(self, project_name, dataset_name, workflow_name):
        self.ui_utils.click_element(self.page_factory.projects_page.create_project_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.fill_input(self.page_factory.projects_page.project_name_input, project_name)  
        self.ui_utils.element_wait_for(self.page_factory.projects_page.create_project_page, state="visible", timeout=10000)
        create_project_page_visible = self.ui_utils.is_element_visible(self.page_factory.projects_page.create_project_page, timeout=10000)
        print(f"Create Project page visibility: {create_project_page_visible}")
        if create_project_page_visible:
            print("Create Project page is visible")
        else:
            raise Exception("Select Dataset button is not visible after clicking the Create Project button.")
        self.ui_utils.click_element(self.page_factory.projects_page.select_dataset)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.projects_page.select_dropdowns(dataset_name))
        self.ui_utils.click_element(self.page_factory.projects_page.heading_create_project)
        self.ui_utils.click_element(self.page_factory.projects_page.select_workflow)
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.projects_page.select_dropdowns(workflow_name))
        self.ui_utils.click_element(self.page_factory.projects_page.heading_create_project)
        create_project_enabled = self.ui_utils.is_element_enabled(self.page_factory.projects_page.create_project_btn)
        print(f"Create Project button enabled: {create_project_enabled}")
        if create_project_enabled:
            print("Create Project button is enabled")
        else:
            raise Exception("Create Project button is not enabled after selecting the dataset and workflow.")
        self.ui_utils.click_element(self.page_factory.projects_page.create_project_btn)

    def click_teams_tab(self):
        self.ui_utils.click_element(self.page_factory.projects_page.teams_tab)
        self.ui_utils.smart_wait()
        teams_panel_visible = self.ui_utils.is_element_visible(self.page_factory.projects_page.teams_panel)
        print(f"Teams panel visibility: {teams_panel_visible}")
        if teams_panel_visible:
            print("Teams panel is visible")
        else:
            raise Exception("Teams panel is not visible after clicking the Teams tab.")

    def add_users(self, role, email_address):
        self.ui_utils.click_element(self.page_factory.projects_page.add_user_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.select_option(self.page_factory.projects_page.assign_user_dropdown, role.upper())
        self.ui_utils.click_element(self.page_factory.projects_page.get_user_checkbox(email_address))
        self.ui_utils.smart_wait()
        self.ui_utils.click_element(self.page_factory.projects_page.add_btn)
        self.ui_utils.smart_wait()
        add_user_btn_visible = self.ui_utils.is_element_visible(self.page_factory.projects_page.add_user_btn)
        print(f"Add user button visibility: {add_user_btn_visible}")
        if add_user_btn_visible:
            print("Add user button is visible")
        else:
            raise Exception("Add user button is not visible after adding the user.")


