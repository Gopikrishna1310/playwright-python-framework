from utils.ui_utils import UIUtils

class ProjectsPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.project_menu         = page.get_by_role("link", name="Projects")
        self.create_project_btn    = page.get_by_role("button", name="Create Project")
        self.delete_toolbar_btn    = page.get_by_role("button", name="Delete")
        self.projects_heading      = page.get_by_role("heading", name="Projects")
        self.project_name_input = page.get_by_role('textbox', name= 'Enter Project Name' )
        self.select_dataset = page.get_by_role('button', name= 'Select Datasets' )
        self.select_workflow = page.get_by_role('button', name= 'Select Workflow' )
        self.create_project_page = page.get_by_text('PlaceholderProject Name*:')
        self.heading_create_project = page.get_by_role('heading', name= 'Create Project' )
        self.project_names_list = page.locator('div[class*="medium text"]')
        self.task_panel = page.get_by_role('tabpanel', name= 'Tasks' )
        self.teams_tab = page.get_by_role('tab', name= 'Teams' )
        self.teams_panel = page.get_by_text('TeamsAdd UsersRemove Selected')
        self.add_user_btn = page.get_by_role('button', name= 'Add Users' )
        self.assign_user_dropdown = page.get_by_role("combobox").first
        self.add_btn = page.get_by_role('button', name='Add' )
        self.assigners_list = page.locator("div[class*='truncate']")
        self.project_delete_success = page.get_by_text('Successfully Deleted Project')
        self.project_description_input = page.get_by_role('textbox', name='Description')
        self.tasks_tab = page.get_by_role('tab', name='Tasks')
        self.project_datasets_tab = page.get_by_role('tab', name='Datasets')
        self.add_datasets_btn = page.get_by_role('button', name='Add')
        self.add_sync_btn = page.get_by_role('button', name='Add/Sync')
        self.dataset_incompatible_toast = page.get_by_text('incompatible', exact=False)
        self.file_name_list_Task_tab = page.locator("td[class*='truncate max'] span")
        self.dataset_name_search = page.get_by_role('textbox', name='Search Datasets')
        self.dataset_name_list = page.locator("td[class*='medium text']")
        

    def select_dropdowns(self, dropdown_name):
        return self.page.get_by_text(dropdown_name, exact=True)

    def click_projects_name(self, dataset_type_name):
        return self.page.get_by_text(dataset_type_name, exact=True)

    def get_user_checkbox(self, email):
        return self.page.locator(
            f"td[title='{email}']"
        ).locator("..").locator("td.px-6").first

    def get_file_status(self, file_name):
        return self.page.locator(
            f"td[title='{file_name}'] ~ td div"
        )