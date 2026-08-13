from pathlib import Path
from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils

class TemplatesActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)

    def click_templates_menu(self):
        self.ui_utils.click_element(self.page_factory.templates_page.templates_menu)
        self.ui_utils.element_wait_for(self.page_factory.templates_page.upload_new_template_btn, state="visible", timeout=10000)
        upload_new_template_btn_visible = self.ui_utils.is_element_visible(self.page_factory.templates_page.upload_new_template_btn, timeout=10000)
        print(f"Upload New Template button visibility: {upload_new_template_btn_visible}")
        if upload_new_template_btn_visible:
            print("Upload New Template button is visible")
        else:
            raise Exception("Upload New Template button is not visible after clicking the Templates menu.")

    def upload_new_template(self, template_name):
        self.ui_utils.click_element(self.page_factory.templates_page.upload_new_template_btn)
        self.ui_utils.smart_wait()
        self.ui_utils.fill_input(self.page_factory.templates_page.template_name_input, template_name)

    def upload_files(self, *file_paths):
            files = []
            for file_path in file_paths:
                full_path = Path("test_data") / "files" / file_path
                if not full_path.exists():
                    raise FileNotFoundError(f"File not found: {full_path}")
                files.append(str(full_path))
            self.page_factory.templates_page.file_upload.set_input_files(files)
            self.ui_utils.smart_wait()
            self.ui_utils.click_element(self.page_factory.templates_page.upload_button)
            self.ui_utils.smart_wait()

        
        