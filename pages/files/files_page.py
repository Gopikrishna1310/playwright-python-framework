import re

from playwright.sync_api import Page

from pages.common.base_page import BasePage


class FilesPage(BasePage):

    def __init__(self, page: Page):

        super().__init__(page)

        self.files_menu = page.get_by_role(
            "link",
            name="Files"
        )

    # ============================================
    # OPEN FILES PAGE
    # ============================================

    def open_files_page(self):

        self.safe_click(
            self.files_menu
        )

        self.page.wait_for_timeout(2000)

        print("\nFiles page opened")

    # ============================================
    # VALIDATE FILES PAGE
    # ============================================

    def validate_files_page_opened(self):

        self.page.wait_for_url(
            "**/files",
            timeout=60000
        )

        print(
            f"\nCurrent URL: {self.page.url}"
        )

        print(
            "\nFiles page validation successful"
        )

    # ============================================
    # OPEN UPLOAD FILES POPUP
    # ============================================

    def open_upload_files_popup(self):

        upload_button = self.page.get_by_role(
            "button",
            name="Upload Files"
        )

        self.safe_click(
            upload_button
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nUpload Files popup opened"
        )

    # ============================================
    # GET FILE INPUT
    # ============================================

    def get_file_input(self):

        upload_area = (
            self.page
            .get_by_test_id("flowbite-label")
            .locator("div")
            .filter(
                has_text="Click to upload from this device"
            )
        )

        upload_area.wait_for(
            state="visible",
            timeout=60000
        )

        return self.page.locator(
            'input[type="file"]'
        )

    # ============================================
    # UPLOAD SINGLE FILE
    # ============================================

    def upload_single_file(
        self,
        file_path
    ):

        file_input = self.get_file_input()

        file_input.set_input_files(
            file_path
        )

        self.page.wait_for_timeout(2000)

        print(
            f"\nSingle file selected:\n{file_path}"
        )

    # ============================================
    # UPLOAD MULTIPLE FILES
    # ============================================

    def upload_multiple_files(
        self,
        file_paths
    ):

        file_input = self.get_file_input()

        file_input.set_input_files(
            file_paths
        )

        self.page.wait_for_timeout(3000)

        print(
            f"\nMultiple files selected simultaneously:\n{file_paths}"
        )

        print(
            f"\nTotal files selected: {len(file_paths)}"
        )

    # ============================================
    # UPLOAD INVALID FILE
    # ============================================

    def upload_invalid_file(
        self,
        file_path
    ):

        file_input = self.get_file_input()

        file_input.set_input_files(
            file_path
        )

        self.page.wait_for_timeout(2000)

        print(
            f"\nInvalid file selected:\n{file_path}"
        )

    # ============================================
    # CLICK UPLOAD BUTTON
    # ============================================

    def click_upload_button(self):

        upload_button = self.page.get_by_role(
            "button",
            name="Upload"
        ).nth(1)

        self.safe_click(
            upload_button
        )

        # Upload processing stabilization
        self.page.wait_for_timeout(5000)

        print(
            "\nUpload button clicked"
        )

    # ============================================
    # VALIDATE UPLOADED FILE
    # ============================================

    def validate_uploaded_file(
        self,
        file_name
    ):

        uploaded_file = (
            self.page
            .get_by_text(file_name)
            .first
        )

        uploaded_file.wait_for(
            state="visible",
            timeout=60000
        )

        print(
            f"\nUploaded file validated:\n{file_name}"
        )

    # ============================================
    # VALIDATE INVALID FILE ERROR
    # ============================================

    def validate_invalid_file_error(self):

        error_message = self.page.get_by_text(
            "Invalid file type. Only allowed file types are permitted."
        )

        error_message.wait_for(
            state="visible",
            timeout=60000
        )

        print(
            "\nInvalid file type validation successful"
        )

    # ============================================
    # OPEN IMPORT FROM S3
    # ============================================

    def open_import_from_s3(self):

        import_button = self.page.get_by_role(
            "button",
            name="Import from S3"
        )

        self.safe_click(
            import_button
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nImport from S3 opened"
        )

    # ============================================
    # SELECT S3 INTEGRATION
    # ============================================

    def select_s3_integration(self):

        integration_dropdown = self.page.get_by_role(
            "combobox"
        )

        integration_dropdown.wait_for(
            state="visible",
            timeout=60000
        )

        integration_dropdown.select_option(
            "1"
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nS3 integration selected"
        )

    # ============================================
    # OPEN S3 FILE PICKER
    # ============================================

    def open_s3_file_picker(self):

        s3_upload_button = self.page.get_by_role(
            "button",
            name="Click to upload from S3"
        )

        self.safe_click(
            s3_upload_button
        )

        self.page.wait_for_timeout(3000)

        print(
            "\nS3 file picker opened"
        )

    # ============================================
    # SELECT FILES FROM S3
    # ============================================

    def select_s3_files(self):

        rows = [19, 20, 21, 22]

        for row in rows:

            checkbox = self.page.locator(
                f"tr:nth-child({row}) > .px-3.py-2\\.5.w-16 > .rounded"
            )

            checkbox.check()

            self.page.wait_for_timeout(500)

        self.page.wait_for_timeout(2000)

        print(
            "\nS3 files selected"
        )

    # ============================================
    # CLICK S3 UPLOAD BUTTON
    # ============================================

    def click_s3_upload_button(self):

        upload_button = self.page.get_by_role(
            "button",
            name="Upload"
        ).first

        self.safe_click(
            upload_button
        )

        # S3 import processing
        self.page.wait_for_timeout(5000)

        print(
            "\nS3 import upload clicked"
        )

    # ============================================
    # CLOSE UPLOAD POPUP
    # ============================================

    def close_upload_popup(self):

        close_button = (
            self.page
            .get_by_role("button")
            .filter(
                has_text=re.compile(r"^$")
            )
            .last
        )

        self.safe_click(
            close_button
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nUpload popup closed"
        )

    # ============================================
    # SELECT FILE CHECKBOX
    # ============================================

    def select_file_checkbox(
        self,
        file_name
    ):

        self.search_file(file_name)

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

        self.page.wait_for_timeout(2000)

        self.clear_search()

        print(
            f"\nSelected file:\n{file_name}"
        )

    # ============================================
    # CLICK DELETE BUTTON
    # ============================================

    def click_delete_button(self):

        delete_button = self.page.get_by_role(
            "button",
            name="Delete"
        )

        self.safe_click(
            delete_button
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nDelete button clicked"
        )

    # ============================================
    # ENTER DELETE CONFIRMATION
    # ============================================

    def enter_delete_confirmation(self):

        delete_input = self.page.get_by_role(
            "textbox"
        )

        self.safe_fill(
            delete_input,
            "DELETE"
        )

        self.page.wait_for_timeout(1000)

        print(
            "\nDELETE confirmation entered"
        )

    # ============================================
    # CONFIRM DELETE
    # ============================================

    def confirm_delete(self):

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

        self.page.wait_for_timeout(3000)

        print(
            "\nDelete confirmed"
        )

    # ============================================
    # SEARCH FILE
    # ============================================

    def search_file(
        self,
        file_name
    ):

        search_box = self.page.get_by_placeholder(
            "search"
        )

        self.safe_fill(
            search_box,
            file_name
        )

        self.page.wait_for_timeout(3000)

        print(
            f"\nSearched file:\n{file_name}"
        )

    # ============================================
    # CLEAR SEARCH
    # ============================================

    def clear_search(self):

        search_box = self.page.get_by_placeholder(
            "search"
        )

        search_box.clear()

        self.page.wait_for_timeout(2000)

        print(
            "\nSearch cleared"
        )