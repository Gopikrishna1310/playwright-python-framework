import re

from playwright.sync_api import Page, expect

from config.urls import BASE_URL
from pages.common.base_page import BasePage
from utils.waits import SHORT, DEFAULT, LONG


class AnnotatorPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # =========================================================================
    # OPEN LOGIN PAGE
    # =========================================================================

    def open_login_page(self):
        self.page.context.grant_permissions(["microphone"], origin=BASE_URL)
        self.page.goto(f"{BASE_URL}/login")

    # =========================================================================
    # LOGIN
    # =========================================================================

    def login(self, email, password):
        self.safe_fill(self.page.get_by_role("textbox", name="Email"), email)
        self.safe_fill(self.page.get_by_role("textbox", name="Password"), password)
        self.safe_click(self.page.get_by_role("button", name="Sign in"))
        print("\nAnnotator login submitted")

    # =========================================================================
    # SELECT ORGANIZATION & ROLE
    # =========================================================================

    def select_organization_and_role(self):
        org_locator = self.page.locator("div").filter(
            has_text=re.compile(r"^ObjectwaysYour roles: Annotator$")
        ).nth(4)
        self.safe_click(org_locator)
        print("\nOrganization selected")

        role_locator = self.page.locator("div").filter(
            has_text=re.compile(r"^Annotator$")
        ).nth(1)
        self.wait.for_visible(role_locator, timeout=DEFAULT)
        self.safe_click(role_locator)
        print("\nAnnotator role selected")

        continue_button = self.page.get_by_role("button", name="Continue")
        self.wait.for_visible(continue_button, timeout=DEFAULT)
        self.safe_click(continue_button)
        print("\nContinue clicked")

    # =========================================================================
    # VALIDATE LOGIN
    # =========================================================================

    def validate_annotator_login(self):
        expect(self.page).to_have_url(re.compile(r".*/tasks"), timeout=LONG)
        expect(self.page.get_by_text("Home")).to_be_visible(timeout=LONG)
        expect(self.page.get_by_role("link", name="Tasks")).to_be_visible(timeout=LONG)
        print("\nAnnotator login validated")

    # =========================================================================
    # OPEN TASK
    # =========================================================================

    def open_task(self, task_name):
        cell = self.page.get_by_role("cell", name=task_name).first
        self.wait.for_visible(cell, timeout=LONG)
        self.safe_click(cell)
        print(f"\nTask opened: {task_name}")

        claim_button = self.page.get_by_role("button", name="Claim Task")
        iframe = self.page.locator("iframe").first
        self.wait.for_visible(claim_button.or_(iframe), timeout=LONG)

    # =========================================================================
    # CLAIM TASK
    # =========================================================================

    def claim_task(self):
        claim_button = self.page.get_by_role("button", name="Claim Task")
        self.wait.for_visible(claim_button, timeout=LONG)
        self.safe_click(claim_button)
        print("\nTask claimed successfully")

    # =========================================================================
    # WAIT FOR TEMPLATE LOAD
    # =========================================================================

    def wait_for_template_load(self):
        frame = self.page.locator("iframe").first.content_frame
        expect(frame.get_by_text("Begin Recording")).to_be_visible(timeout=LONG)
        expect(frame.locator("text=0:00 /")).to_be_visible(timeout=LONG)
        self.page.wait_for_timeout(5000)
        print("\nAudio template fully loaded")

    # =========================================================================
    # CREATE AUDIO ANNOTATION
    # =========================================================================

    def create_audio_annotation(self, transcription_text):
        self.wait_for_template_load()

        frame = self.page.locator("iframe").first.content_frame

        self.safe_click(frame.get_by_text("Begin Recording"))
        print("\nRecording started")

        self.page.wait_for_timeout(5000)

        self.safe_click(frame.get_by_text("Stop Recording"))
        print("\nRecording stopped")

        transcription_input = frame.get_by_role(
            "textbox", name="Enter transcription text"
        )
        self.wait.for_visible(transcription_input, timeout=LONG)
        self.safe_fill(transcription_input, transcription_text)
        print("\nTranscription entered")

        set_text_button = frame.get_by_role("button", name="Set Text")
        expect(set_text_button).to_be_enabled(timeout=DEFAULT)
        self.safe_click(set_text_button)
        print("\nAnnotation created successfully")

        submit_button = frame.get_by_role("button", name="Submit Annotation")
        self.wait.for_visible(submit_button, timeout=LONG)

    # =========================================================================
    # SUBMIT ANNOTATION
    # =========================================================================

    def submit_annotation(self):
        frame = self.page.locator("iframe").first.content_frame
        submit_button = frame.get_by_role("button", name="Submit Annotation")
        self.safe_click(submit_button)
        print("\nAnnotation submitted successfully")

        try:
            self.wait.for_hidden(submit_button, timeout=SHORT)
            print("  Submit button hidden after click")
        except Exception:
            print("  Submit button still visible after click (may be disabled)")

    # =========================================================================
    # RELEASE TASK
    # =========================================================================

    def release_task(self):
        self.safe_click(self.page.get_by_role("button", name="Release").first)
        print("\nRelease popup opened")

        popup_release_button = self.page.locator(
            "div[role='dialog']"
        ).get_by_role("button", name="Release")
        self.wait.for_visible(popup_release_button, timeout=DEFAULT)
        self.safe_click(popup_release_button)
        print("\nTask released successfully")

        try:
            self.wait.for_hidden(
                self.page.locator("div[role='dialog']"), timeout=SHORT
            )
        except Exception:
            pass

    # =========================================================================
    # LOGOUT
    # =========================================================================

    def logout(self):
        self.safe_click(
            self.page.locator("div").filter(
                has_text=re.compile(r"^A$")
            ).nth(2)
        )
        print("\nProfile menu opened")

        logout_button = self.page.get_by_role("button", name="Logout")
        self.wait.for_visible(logout_button, timeout=DEFAULT)
        self.safe_click(logout_button)

        expect(self.page).to_have_url(re.compile(r".*/login"), timeout=LONG)
        print("\nLogout successful")