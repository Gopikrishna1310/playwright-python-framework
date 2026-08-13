from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils
from utils.helpers import Helpers

class AnnotatorActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)
        self.helpers = Helpers(page)

    def annontate_files(self, input_text):
        self.ui_utils.element_wait_for(self.page_factory.annotator_page.begin_recording, timeout = 10000)
        self.ui_utils.click_element(self.page_factory.annotator_page.begin_recording)
        self.ui_utils.smart_wait()
        self.ui_utils.element_wait_for(self.page_factory.annotator_page.stop_recording, timeout = 10000)
        self.ui_utils.click_element(self.page_factory.annotator_page.stop_recording)
        self.ui_utils.click_element(self.page_factory.annotator_page.input_text_field)
        self.ui_utils.fill_input(self.page_factory.annotator_page.input_text_field, input_text)
        self.ui_utils.click_element(self.page_factory.annotator_page.set_text_button)
        self.ui_utils.smart_wait()