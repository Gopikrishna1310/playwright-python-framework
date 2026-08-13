from utils.ui_utils import UIUtils

class TemplatesPage:
    def __init__(self, page):
        self.page = page
        self.ui_utils = UIUtils(page)

        self.templates_menu          = page.get_by_role("link", name="Templates")
        self.upload_new_template_btn = page.get_by_role("button", name="Upload New Template")
        self.template_name_input = page.get_by_role('textbox', name= 'Template Name * Upload file *')
        self.file_upload = page.locator('label').filter(has_text='Click to upload')
        self.upload_button = page.get_by_role('button', name= 'Upload')
        self.template_names_list = page.locator('div[class*="medium text"]')#Changed