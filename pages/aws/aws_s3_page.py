from playwright.sync_api import Page

from pages.common.base_page import BasePage
from utils.waits import DEFAULT, LONG, LOAD


class AWSS3Page(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # =========================================================================
    # OPEN S3 CONSOLE
    # =========================================================================

    def open_s3_console(self):
        self.page.goto(
            "https://s3.console.aws.amazon.com/s3/home",
            wait_until="domcontentloaded",
            timeout=LOAD,
        )
        self.page.wait_for_url("**/s3/home**", timeout=LONG)
        print("\nS3 Console opened")

    # =========================================================================
    # SEARCH BUCKET
    # =========================================================================

    def search_bucket(self, bucket_name):
        search_input = self.page.get_by_placeholder("Find buckets by name")
        self.wait.for_visible(search_input, timeout=LONG)
        self.safe_fill(search_input, bucket_name)
        print("\nBucket searched")

    # =========================================================================
    # OPEN BUCKET
    # =========================================================================

    def open_bucket(self, bucket_name):
        bucket_link = self.page.get_by_role("link", name=bucket_name)
        self.wait.for_visible(bucket_link, timeout=LONG)
        self.safe_click(bucket_link)
        print("\nBucket opened")

    # =========================================================================
    # OPEN PERMISSIONS TAB
    # =========================================================================

    def open_permissions_tab(self):
        permissions_tab = self.page.get_by_role("tab", name="Permissions")
        self.wait.for_visible(permissions_tab, timeout=LONG)
        self.safe_click(permissions_tab)
        print("\nPermissions tab opened")

    # =========================================================================
    # CLICK EDIT CORS
    # =========================================================================

    def click_edit_cors(self):
        edit_button = self.page.get_by_role("button", name="Edit").last
        self.wait.for_visible(edit_button, timeout=LONG)
        self.safe_click(edit_button)
        print("\nCORS Edit opened")

    # =========================================================================
    # REPLACE CORS JSON
    # =========================================================================

    def replace_cors_json(self, cors_json):
        editor = self.page.locator(".ace_content")
        self.wait.for_visible(editor, timeout=LONG)
        editor.click(force=True)
        self.page.keyboard.press("Control+A")
        self.page.keyboard.press("Backspace")
        self.page.keyboard.insert_text(cors_json)
        self.verify_contains_text(editor, "AllowedOrigins", timeout=DEFAULT)
        print("\nCORS JSON pasted")

    # =========================================================================
    # SAVE CORS CHANGES
    # =========================================================================

    def save_changes(self):
        save_button = self.page.get_by_role("button", name="Save changes")
        self.wait.for_visible(save_button, timeout=LONG)
        self.safe_click(save_button)
        self.wait.for_hidden(save_button, timeout=LONG)
        print("\nCORS changes saved")

    # =========================================================================
    # OPEN OBJECTS TAB
    # =========================================================================

    def open_objects_tab(self):
        objects_tab = self.page.get_by_role("tab", name="Objects")
        self.wait.for_visible(objects_tab, timeout=LONG)
        self.safe_click(objects_tab)
        print("\nObjects tab opened")

    # =========================================================================
    # OPEN FIRST FILE
    # =========================================================================

    def open_first_file(self):
        object_link = self.page.locator("table a[href]").nth(0)
        self.wait.for_visible(object_link, timeout=LONG)
        self.scroll_into_view(object_link)
        object_link.dblclick()
        print("\nS3 object opened")

    # =========================================================================
    # COPY S3 URI
    # =========================================================================

    def copy_s3_uri(self):
        self.page.bring_to_front()
        copy_button = (
            self.page
            .get_by_test_id(
                "key-value-group-object_overview_card__key_value_group-container"
            )
            .get_by_role("button", name="Copy S3 URI")
        )
        self.wait.for_visible(copy_button, timeout=LONG)
        self.safe_click(copy_button)
        s3_uri = self.read_clipboard(expected_prefix="s3://")
        print(f"\nS3 URI copied: {s3_uri}")
        return s3_uri