import re

from playwright.sync_api import (
    Page,
    expect
)

from config.urls import BASE_URL


class AnnotatorPage:

    def __init__(self, page: Page):

        self.page = page

    # =====================================================
    # OPEN LOGIN PAGE
    # =====================================================

    def open_login_page(self):

        self.page.goto(
            f"{BASE_URL}/login"
        )

    # =====================================================
    # LOGIN
    # =====================================================

    def login(
            self,
            email,
            password
    ):

        self.page.get_by_role(
            "textbox",
            name="Email"
        ).fill(email)

        self.page.get_by_role(
            "textbox",
            name="Password"
        ).fill(password)

        self.page.get_by_role(
            "button",
            name="Sign in"
        ).click()

        print(
            "\nAnnotator login submitted"
        )

    # =====================================================
    # SELECT ORGANIZATION & ROLE
    # =====================================================

    def select_organization_and_role(self):

        # SELECT ORGANIZATION

        self.page.locator(
            "div"
        ).filter(
            has_text=re.compile(
                r"^ObjectwaysYour roles: Annotator$"
            )
        ).nth(4).click()

        print(
            "\nOrganization selected"
        )

        self.page.wait_for_timeout(2000)

        # SELECT ROLE

        self.page.locator(
            "div"
        ).filter(
            has_text=re.compile(
                r"^Annotator$"
            )
        ).nth(1).click()

        print(
            "\nAnnotator role selected"
        )

        self.page.wait_for_timeout(1000)

        # CONTINUE

        self.page.get_by_role(
            "button",
            name="Continue"
        ).click()

        print(
            "\nContinue clicked"
        )

    # =====================================================
    # VALIDATE LOGIN
    # =====================================================

    def validate_annotator_login(self):

        expect(
            self.page
        ).to_have_url(
            re.compile(r".*/tasks")
        )

        expect(
            self.page.get_by_text(
                "Home"
            )
        ).to_be_visible()

        expect(
            self.page.get_by_role(
                "link",
                name="Tasks"
            )
        ).to_be_visible()

    # =====================================================
    # OPEN TASK
    # =====================================================

    def open_task(
            self,
            task_name
    ):

        self.page.get_by_role(
            "cell",
            name=task_name
        ).first.click()

        print(
            f"\nTask opened: {task_name}"
        )

        self.page.wait_for_timeout(3000)

    # =====================================================
    # CLAIM TASK
    # =====================================================

    def claim_task(self):

        claim_button = self.page.get_by_role(
            "button",
            name="Claim Task"
        )

        if claim_button.is_visible():

            claim_button.click()

            print(
                "\nTask claimed successfully"
            )

        else:

            print(
                "\nTask already claimed"
            )

        self.page.wait_for_timeout(3000)

    # =====================================================
    # WAIT FOR TEMPLATE LOAD
    # =====================================================

    def wait_for_template_load(self):

        frame = self.page.locator(
            "iframe"
        ).first.content_frame

        # WAIT FOR RECORD BUTTON

        expect(
            frame.get_by_text(
                "Begin Recording"
            )
        ).to_be_visible(
            timeout=60000
        )

        # WAIT FOR AUDIO PLAYER

        expect(
            frame.locator(
                "text=0:00 /"
            )
        ).to_be_visible(
            timeout=60000
        )

        # EXTRA WAIT

        self.page.wait_for_timeout(5000)

        print(
            "\nAudio template fully loaded"
        )

    # =====================================================
    # CREATE AUDIO ANNOTATION
    # =====================================================

    def create_audio_annotation(
            self,
            transcription_text
    ):

        self.wait_for_template_load()

        frame = self.page.locator(
            "iframe"
        ).first.content_frame

        # START RECORDING

        frame.get_by_text(
            "Begin Recording"
        ).click()

        print(
            "\nRecording started"
        )

        self.page.wait_for_timeout(5000)

        # STOP RECORDING

        frame.get_by_text(
            "Stop Recording"
        ).click()

        print(
            "\nRecording stopped"
        )

        self.page.wait_for_timeout(3000)

        # ENTER TRANSCRIPTION

        frame.get_by_role(
            "textbox",
            name="Enter transcription text"
        ).fill(
            transcription_text
        )

        print(
            "\nTranscription entered"
        )

        # SET TEXT

        frame.get_by_role(
            "button",
            name="Set Text"
        ).click()

        print(
            "\nAnnotation created successfully"
        )

        self.page.wait_for_timeout(3000)

    # =====================================================
    # SUBMIT ANNOTATION
    # =====================================================

    def submit_annotation(self):

        frame = self.page.locator(
            "iframe"
        ).first.content_frame

        frame.get_by_role(
            "button",
            name="Submit Annotation"
        ).click()

        print(
            "\nAnnotation submitted successfully"
        )

        self.page.wait_for_timeout(5000)

    # =====================================================
    # RELEASE TASK
    # =====================================================

    def release_task(self):

        # CLICK TOP RELEASE BUTTON

        self.page.get_by_role(
            "button",
            name="Release"
        ).first.click()

        print(
            "\nRelease popup opened"
        )

        self.page.wait_for_timeout(2000)

        # CLICK POPUP RELEASE BUTTON

        popup_release_button = self.page.locator(
            "div[role='dialog']"
        ).get_by_role(
            "button",
            name="Release"
        )

        popup_release_button.click()

        print(
            "\nTask released successfully"
        )

        self.page.wait_for_timeout(3000)

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self):

        self.page.locator(
            "div"
        ).filter(
            has_text=re.compile(
                r"^A$"
            )
        ).nth(2).click()

        print(
            "\nProfile menu opened"
        )

        self.page.wait_for_timeout(1000)

        self.page.get_by_role(
            "button",
            name="Logout"
        ).click()

        expect(
            self.page
        ).to_have_url(
            re.compile(r".*/login")
        )

        print(
            "\nLogout successful"
        )