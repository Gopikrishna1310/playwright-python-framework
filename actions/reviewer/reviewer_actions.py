from pages.page_factory import PageFactory
from utils.ui_utils import UIUtils
from utils.helpers import Helpers

class ReviewerActions:
    def __init__(self, page):
        self.page_factory = PageFactory(page)
        self.ui_utils = UIUtils(page)
        self.helpers = Helpers(page)

    def is_annotation_present(self, annotator):
        self.ui_utils.click_element(self.page_factory.reviewer_page.annotation_dropdown)
        self.ui_utils.click_element(self.page_factory.reviewer_page.click_annotator_dropdown(annotator))
        self.ui_utils.smart_wait()
