import re

from playwright.sync_api import Page

from pages.common.base_page import BasePage


class DatasetsPage(BasePage):

    def __init__(
            self,
            page: Page
    ):

        super().__init__(page)

        self.datasets_menu = page.get_by_role(
            "link",
            name="Datasets"
        )

    # ============================================
    # OPEN DATASETS PAGE
    # ============================================

    def open_datasets_page(self):

        self.safe_click(
            self.datasets_menu
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nDatasets page opened"
        )

    # ============================================
    # VALIDATE DATASETS PAGE
    # ============================================

    def validate_datasets_page_opened(self):

        self.page.wait_for_url(
            "**/datasets",
            timeout=60000
        )

        print(
            f"\nCurrent URL: {self.page.url}"
        )

        print(
            "\nDatasets page validation successful"
        )

    # ============================================
    # OPEN CREATE DATASET POPUP
    # ============================================

    def open_create_dataset_popup(self):

        create_button = self.page.get_by_role(
            "button",
            name="Create Dataset"
        )

        self.safe_click(
            create_button
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nCreate Dataset popup opened"
        )

    # ============================================
    # ENTER DATASET NAME
    # ============================================

    def enter_dataset_name(
            self,
            dataset_name
    ):

        dataset_input = self.page.get_by_role(
            "textbox",
            name="Enter Dataset Name"
        )

        self.safe_fill(
            dataset_input,
            dataset_name
        )

        self.page.wait_for_timeout(1000)

        print(
            f"\nDataset name entered:\n{dataset_name}"
        )

    # ============================================
    # ENTER DATASET DESCRIPTION
    # ============================================

    def enter_dataset_description(
            self,
            description
    ):

        description_input = self.page.get_by_role(
            "textbox",
            name="Enter Dataset Description"
        )

        if description_input.count() > 0:

            self.safe_fill(
                description_input,
                description
            )

            self.page.wait_for_timeout(1000)

            print(
                f"\nDataset description entered:\n{description}"
            )

    # ============================================
    # SELECT DATASET TYPE
    # ============================================

    def select_dataset_type(
            self,
            dataset_type
    ):

        dropdown = self.page.get_by_role(
            "button",
            name="Text"
        )

        self.safe_click(
            dropdown
        )

        self.page.wait_for_timeout(1000)

        dataset_option = (
            self.page
            .locator("div")
            .filter(
                has_text=re.compile(
                    rf"^{re.escape(dataset_type)}$"
                )
            )
        )

        self.safe_click(
            dataset_option
        )

        self.page.wait_for_timeout(1500)

        print(
            f"\nDataset type selected:\n{dataset_type}"
        )

    # ============================================
    # CLICK CREATE BUTTON
    # ============================================

    def click_create_dataset_button(self):

        create_button = self.page.get_by_role(
            "button",
            name="Create"
        )

        self.safe_click(
            create_button
        )

        # Backend dataset creation stabilization
        self.page.wait_for_timeout(3000)

        print(
            "\nCreate dataset button clicked"
        )

    # ============================================
    # VALIDATE DATASET CREATED
    # ============================================

    def validate_dataset_created(
            self,
            dataset_name
    ):

        dataset_row = self.page.get_by_text(
            dataset_name
        ).first

        dataset_row.wait_for(
            state="visible",
            timeout=60000
        )

        print(
            f"\nDataset validated:\n{dataset_name}"
        )

    # ============================================
    # COMPLETE DATASET CREATION FLOW
    # ============================================

    def create_dataset(
            self,
            dataset_name,
            dataset_type,
            description=""
    ):

        self.open_create_dataset_popup()

        self.enter_dataset_name(
            dataset_name
        )

        if dataset_type != "Text":

            self.select_dataset_type(
                dataset_type
            )

        if description:

            self.enter_dataset_description(
                description
            )

        self.click_create_dataset_button()

        self.validate_dataset_created(
            dataset_name
        )

    # ============================================
    # OPEN DATASET
    # ============================================

    def open_dataset(
            self,
            dataset_name
    ):

        dataset = self.page.get_by_text(
            dataset_name
        ).first

        self.safe_click(
            dataset
        )

        self.page.wait_for_timeout(3000)

        print(
            f"\nDataset opened:\n{dataset_name}"
        )

    # ============================================
    # OPEN ADD FILES POPUP
    # ============================================

    def open_add_files_popup(self):

        add_files_button = self.page.get_by_role(
            "button",
            name="Add Files"
        )

        self.safe_click(
            add_files_button
        )

        self.page.wait_for_timeout(3000)

        print(
            "\nAdd Files popup opened"
        )

    # ============================================
    # SELECT FILE FOR DATASET
    # ============================================

    def select_dataset_file(
            self,
            file_name
    ):

        file_row = self.page.get_by_role(
            "row",
            name=re.compile(
                re.escape(file_name),
                re.IGNORECASE
            )
        ).first

        file_row.wait_for(
            state="visible",
            timeout=60000
        )

        checkbox = file_row.get_by_role(
            "checkbox"
        )

        checkbox.check()

        self.page.wait_for_timeout(1500)

        print(
            f"\nDataset file selected:\n{file_name}"
        )

    # ============================================
    # CLICK ADD FILES BUTTON
    # ============================================

    def click_add_files_button(self):

        add_button = (
            self.page
            .get_by_role(
                "button",
                name="Add Files"
            )
            .last
        )

        self.safe_click(
            add_button
        )

        # Backend file linking stabilization
        self.page.wait_for_timeout(4000)

        print(
            "\nAdd Files confirmed"
        )

    # ============================================
    # VALIDATE FILE ADDED TO DATASET
    # ============================================

    def validate_dataset_file(
            self,
            file_name
    ):

        added_file = self.page.get_by_text(
            file_name
        ).first

        added_file.wait_for(
            state="visible",
            timeout=60000
        )

        print(
            f"\nDataset file validated:\n{file_name}"
        )

    # ============================================
    # SELECT DATASET FILE CHECKBOX
    # ============================================

    def select_dataset_file_checkbox(
            self,
            file_name
    ):

        file_row = self.page.get_by_role(
            "row",
            name=re.compile(
                re.escape(file_name),
                re.IGNORECASE
            )
        ).first

        file_row.wait_for(
            state="visible",
            timeout=60000
        )

        checkbox = file_row.get_by_role(
            "checkbox"
        )

        checkbox.check()

        self.page.wait_for_timeout(1500)

        print(
            f"\nDataset file selected for delete:\n{file_name}"
        )

    # ============================================
    # CLICK DELETE BUTTON
    # ============================================

    def click_delete_dataset_file_button(self):

        delete_button = self.page.get_by_role(
            "button",
            name="Delete"
        )

        self.safe_click(
            delete_button
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nDataset delete button clicked"
        )

    # ============================================
    # ENTER DELETE CONFIRMATION
    # ============================================

    def enter_dataset_delete_confirmation(self):

        delete_input = self.page.get_by_role(
            "textbox"
        )

        self.safe_fill(
            delete_input,
            "DELETE"
        )

        self.page.wait_for_timeout(1000)

        print(
            "\nDataset DELETE confirmation entered"
        )

    # ============================================
    # CONFIRM DELETE
    # ============================================

    def confirm_dataset_file_delete(self):

        confirm_button = (
            self.page
            .get_by_role(
                "button",
                name="Delete"
            )
            .last
        )

        self.safe_click(
            confirm_button
        )

        # Backend delete propagation
        self.page.wait_for_timeout(4000)

        print(
            "\nDataset file delete confirmed"
        )

    # ============================================
    # CLOSE DELETE SUMMARY POPUP
    # ============================================

    def close_delete_summary_popup(self):

        close_button = (
            self.page
            .locator("button")
            .filter(
                has=self.page.locator("svg")
            )
            .last
        )

        self.safe_click(
            close_button
        )

        self.page.wait_for_timeout(1500)

        print(
            "\nDelete summary popup closed"
        )

    # ============================================
    # SELECT DATASET CHECKBOX
    # ============================================

    def select_dataset_checkbox(
            self,
            dataset_name
    ):

        dataset_row = self.page.get_by_role(
            "row",
            name=re.compile(
                re.escape(dataset_name),
                re.IGNORECASE
            )
        ).first

        dataset_row.wait_for(
            state="visible",
            timeout=60000
        )

        checkbox = dataset_row.get_by_role(
            "checkbox"
        )

        checkbox.check()

        self.page.wait_for_timeout(1500)

        print(
            f"\nDataset selected for delete:\n{dataset_name}"
        )

    # ============================================
    # CLICK DELETE DATASET BUTTON
    # ============================================

    def click_delete_dataset_button(self):

        delete_button = self.page.get_by_role(
            "button",
            name="Delete"
        )

        self.safe_click(
            delete_button
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nDataset delete button clicked"
        )

    # ============================================
    # ENTER DATASET DELETE CONFIRMATION
    # ============================================

    def enter_dataset_confirmation(self):

        delete_input = self.page.get_by_role(
            "textbox"
        )

        self.safe_fill(
            delete_input,
            "DELETE"
        )

        self.page.wait_for_timeout(1000)

        print(
            "\nDataset DELETE confirmation entered"
        )

    # ============================================
    # CONFIRM DATASET DELETE
    # ============================================

    def confirm_dataset_delete(self):

        confirm_button = (
            self.page
            .get_by_role(
                "button",
                name="Delete"
            )
            .last
        )

        self.safe_click(
            confirm_button
        )

        # Backend dataset delete stabilization
        self.page.wait_for_timeout(4000)

        print(
            "\nDataset delete confirmed"
        )