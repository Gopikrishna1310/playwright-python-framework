from playwright.sync_api import (
    Page
)

from pages.common.base_page import (
    BasePage
)


class AWSS3Page(BasePage):

    def __init__(self, page: Page):

        super().__init__(page)

    # ============================================
    # OPEN S3 CONSOLE
    # ============================================

    def open_s3_console(self):

        self.page.goto(
            "https://s3.console.aws.amazon.com/s3/home"
        )

        self.page.wait_for_load_state()

        self.page.wait_for_url(
            "**/s3/home**",
            timeout=60000
        )

        # S3 rendering stabilization
        self.page.wait_for_timeout(3000)

        print("\nS3 Console opened")

    # ============================================
    # SEARCH BUCKET
    # ============================================

    def search_bucket(
        self,
        bucket_name
    ):

        search_input = self.page.get_by_placeholder(
            "Find buckets by name"
        )

        search_input.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_fill(
            search_input,
            bucket_name
        )

        # S3 table refresh
        self.page.wait_for_timeout(2000)

        print("\nBucket searched")

    # ============================================
    # OPEN BUCKET
    # ============================================

    def open_bucket(
        self,
        bucket_name
    ):

        bucket_link = self.page.get_by_role(
            "link",
            name=bucket_name
        )

        bucket_link.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            bucket_link
        )

        # Bucket page stabilization
        self.page.wait_for_timeout(2000)

        print("\nBucket opened")

    # ============================================
    # OPEN PERMISSIONS TAB
    # ============================================

    def open_permissions_tab(self):

        permissions_tab = self.page.get_by_role(
            "tab",
            name="Permissions"
        )

        permissions_tab.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            permissions_tab
        )

        # Permissions content rendering
        self.page.wait_for_timeout(2000)

        print("\nPermissions tab opened")

    # ============================================
    # CLICK EDIT CORS
    # ============================================

    def click_edit_cors(self):

        edit_button = self.page.get_by_role(
            "button",
            name="Edit"
        ).last

        edit_button.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            edit_button
        )

        # ACE editor rendering
        self.page.wait_for_timeout(2000)

        print("\nCORS Edit opened")

    # ============================================
    # REPLACE CORS JSON
    # ============================================

    def replace_cors_json(
        self,
        cors_json
    ):

        # ========================================
        # ACE EDITOR
        # ========================================

        editor = self.page.locator(
            ".ace_content"
        )

        editor.wait_for(
            state="visible",
            timeout=60000
        )

        editor.click(
            force=True
        )

        self.page.wait_for_timeout(1000)

        # ========================================
        # SELECT ALL
        # ========================================

        self.page.keyboard.press(
            "Control+A"
        )

        self.page.wait_for_timeout(500)

        # ========================================
        # DELETE OLD JSON
        # ========================================

        self.page.keyboard.press(
            "Backspace"
        )

        self.page.wait_for_timeout(500)

        # ========================================
        # INSERT NEW JSON
        # ========================================

        self.page.keyboard.insert_text(
            cors_json
        )

        # Editor update stabilization
        self.page.wait_for_timeout(1500)

        print("\nCORS JSON pasted")

    # ============================================
    # SAVE CORS CHANGES
    # ============================================

    def save_changes(self):

        save_button = self.page.get_by_role(
            "button",
            name="Save changes"
        )

        save_button.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            save_button
        )

        # Save propagation stabilization
        self.page.wait_for_timeout(3000)

        print("\nCORS changes saved")

    # ============================================
    # OPEN OBJECTS TAB
    # ============================================

    def open_objects_tab(self):

        objects_tab = self.page.get_by_role(
            "tab",
            name="Objects"
        )

        objects_tab.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            objects_tab
        )

        # Object table rendering
        self.page.wait_for_timeout(2000)

        print("\nObjects tab opened")

    # ============================================
    # OPEN FIRST FILE
    # ============================================

    def open_first_file(self):

        object_link = self.page.locator(
            'table a[href]'
        ).nth(0)

        object_link.wait_for(
            state="visible",
            timeout=60000
        )

        object_link.scroll_into_view_if_needed()

        self.page.wait_for_timeout(1000)

        object_link.dblclick()

        # Object details rendering
        self.page.wait_for_timeout(3000)

        print("\nS3 object opened")

    # ============================================
    # COPY S3 URI
    # ============================================

    def copy_s3_uri(self):

        copy_button = (
            self.page
            .get_by_test_id(
                "key-value-group-object_overview_card__key_value_group-container"
            )
            .get_by_role(
                "button",
                name="Copy S3 URI"
            )
        )

        copy_button.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            copy_button
        )

        # Clipboard stabilization
        self.page.wait_for_timeout(1000)

        s3_uri = self.page.evaluate(
            "navigator.clipboard.readText()"
        )

        print(
            f"\nS3 URI copied:\n{s3_uri}"
        )

        return s3_uri