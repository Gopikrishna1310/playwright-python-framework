from playwright.sync_api import (
    expect
)


class BasePage:

    def __init__(self, page):

        self.page = page

    # ============================================
    # OPEN URL
    # ============================================

    def open_url(self, url):

        self.page.goto(url)

        self.page.wait_for_load_state(
            "networkidle"
        )

    # ============================================
    # SAFE CLICK
    # ============================================

    def safe_click(self, locator):

        locator.wait_for(
            state="visible"
        )

        locator.click()

    # ============================================
    # SAFE FILL
    # ============================================

    def safe_fill(self, locator, text):

        locator.wait_for(
            state="visible"
        )

        locator.fill(text)

    # ============================================
    # WAIT FOR ELEMENT
    # ============================================

    def wait_for_element(self, locator):

        locator.wait_for(
            state="visible"
        )

    # ============================================
    # VERIFY ELEMENT VISIBLE
    # ============================================

    def verify_visible(self, locator):

        expect(locator).to_be_visible()

    # ============================================
    # VERIFY TEXT
    # ============================================

    def verify_text(
        self,
        locator,
        expected_text
    ):

        expect(locator).to_have_text(
            expected_text
        )

    # ============================================
    # WAIT FOR PAGE LOAD
    # ============================================

    def wait_for_page_load(self):

        self.page.wait_for_load_state(
            "networkidle"
        )

    # ============================================
    # SCROLL INTO VIEW
    # ============================================

    def scroll_into_view(self, locator):

        locator.scroll_into_view_if_needed()

    # ============================================
    # GET TEXT
    # ============================================

    def get_text(self, locator):

        locator.wait_for(
            state="visible"
        )

        return locator.text_content()

    # ============================================
    # PRESS KEY
    # ============================================

    def press_key(self, key):

        self.page.keyboard.press(key)

    # ============================================
    # PRESS KEY
    # ============================================

    def press_key(self, key):

        self.page.keyboard.press(key)

    # ============================================
    # SWITCH TO PAGE
    # ============================================

    def switch_to_page(self, page):

        page.bring_to_front()

        page.wait_for_load_state()

        self.page.wait_for_timeout(1500)