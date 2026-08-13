from utils.ui_utils import UIUtils

class datasetsPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.datasets_menu          = page.get_by_role("link", name="Datasets")
        self.create_dataset_button  = page.get_by_role("button", name="Create Dataset")
        self.enter_dataset_name = page.get_by_role('textbox', name='Enter Dataset Name' )
        self.select_dataset_type = page.get_by_role('button', name='Select Type' )
        self.create_button = page.get_by_role('button', name='Create' )
        self.dataset_names_list = page.locator('span[class*="medium break"]')  #page.locator('span[class*="dataset-name"]')
        self.dataset_cell = page.locator('th:has-text("Dataset Name")')
        self.upload_files_button = page.get_by_role('button',  name='Upload Files')
        self.upload_files = page.locator('label').filter(has_text='Click to upload from this')
        self.upload_button = page.get_by_role('button', name= 'Upload')
        self.files_name_list = page.locator("div[class*='break-all']")  #page.locator("div[class*='dataset-file-name']")


    def get_dataset_type_option(self, dataset_type_name):
        return self.page.get_by_text(dataset_type_name, exact=True)