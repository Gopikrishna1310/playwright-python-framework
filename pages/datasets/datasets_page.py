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
        self.dataset_names_list = page.locator('span[class*="dataset-name"]')
        self.dataset_cell = page.locator('th:has-text("Dataset Name")')
        self.upload_files_button = page.get_by_role('button',  name='Upload Files')
        self.upload_files = page.locator('label').filter(has_text='Click to upload from this')
        self.upload_button = page.get_by_role('button', name= 'Upload',exact = True)
        self.files_name_list = page.locator("button[class*='file-name']")
        self.dataset_file_name_list = page.locator("div[class*='dataset-names']")
        self.dataset_name_error_msg = self.page.get_by_text("Only letters, numbers, spaces, _ and - are allowed", exact=True)
        self.dataset_exists_error = page.get_by_text("A Dataset with this name already exists", exact=True)
        self.add_files = page.get_by_role('button', name='Add Files')
        self.dataset_delete_success_popup = self.page.get_by_text('Successfully Deleted Dataset')
        self.dataset_delete_failed_popup = self.page.get_by_text('Failed Deleted Dataset')
        self.dataset_type_list = self.page.locator("span[class*='text-sm text']")
        self.dataset_description = page.get_by_role('textbox', name='Enter Dataset Description' )


    def get_dataset_type_option(self, dataset_type_name):
        return self.page.get_by_test_id("modal-overlay").get_by_text(dataset_type_name)

    def click_dataset_file_name(self, file_name):
        return self.page.locator("span").filter(has_text=file_name)

    def get_company_name_by_dataset(self, dataset_name):
        return self.page.locator(f"xpath=//span[contains(@class,'dataset-name') and text()='{dataset_name}']//ancestor::td//following-sibling::td//div")