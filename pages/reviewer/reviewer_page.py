import re

from playwright.sync_api import expect
from config.urls import BASE_URL


class ReviewerPage:

    def __init__(self, page):

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

    def login(self, email, password):

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
            "\nReviewer login submitted"
        )

    # =====================================================
    # SELECT ORGANIZATION & ROLE
    # =====================================================

    def select_organization_and_role(self):

        # SELECT ORGANIZATION

        self.page.locator("div").filter(
            has_text=re.compile(
                r"^ObjectwaysYour roles:"
            )
        ).nth(4).click()

        print(
            "\nOrganization selected"
        )

        # SELECT REVIEWER ROLE

        self.page.locator("div").filter(
            has_text=re.compile(
                r"^Reviewer$"
            )
        ).nth(1).click()

        print(
            "\nReviewer role selected"
        )

        # CLICK CONTINUE

        self.page.get_by_role(
            "button",
            name="Continue"
        ).click()

        print(
            "\nContinue clicked"
        )

    # =====================================================
    # VALIDATE REVIEWER LOGIN
    # =====================================================

    def validate_reviewer_login(self):

        expect(
            self.page
        ).to_have_url(
            re.compile(r".*/tasks")
        )

        # VALIDATE HOME SIDEBAR

        expect(
            self.page.get_by_role(
                "link",
                name="Home"
            )
        ).to_be_visible()

        # VALIDATE TASKS SIDEBAR

        expect(
            self.page.get_by_role(
                "link",
                name="Tasks"
            )
        ).to_be_visible()

        print(
            "\nReviewer redirected to Tasks page"
        )

    # =====================================================
    # OPEN TASK
    # =====================================================

    def open_task(self, task_name):

        self.page.get_by_role(
            "cell",
            name=task_name
        ).first.click()

        print(
            f"\nTask opened: {task_name}"
        )

        self.page.wait_for_timeout(5000)

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

        # WAIT FOR REVIEW PAGE TO LOAD

        self.page.wait_for_timeout(5000)

    # =====================================================
    # REJECT TASK
    # =====================================================

    def reject_task(self, comment):

        self.page.get_by_role(
            "button",
            name="Reject"
        ).click()

        print(
            "\nReject popup opened"
        )

        comment_box = self.page.get_by_role(
            "textbox"
        )

        if comment_box.is_visible():

            comment_box.fill(comment)

        self.page.get_by_role(
            "button",
            name="Submit"
        ).click()

        print(
            "\nTask rejected successfully"
        )

    # =====================================================
    # OPEN PROFILE MENU
    # =====================================================

    def open_profile_menu(self):

        self.page.locator("div").filter(
            has_text=re.compile(r"^R$")
        ).nth(2).click()

        print(
            "\nProfile menu opened"
        )

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self):

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
            "\nReviewer logout successful"
        )

    # =====================================================
    # APPROVE TASK
    # =====================================================

    def approve_task(self):

        # CLICK APPROVE

        self.page.get_by_role(
            "button",
            name="Approve"
        ).click()

        print(
            "\nApprove confirmation popup opened"
        )

        # FIRST OK BUTTON

        self.page.once(
            "dialog",
            lambda dialog: dialog.accept()
        )

        self.page.get_by_role(
            "button",
            name="Approve"
        ).click()

        self.page.wait_for_timeout(2000)

        # SECOND SUCCESS POPUP

        self.page.once(
            "dialog",
            lambda dialog: dialog.accept()
        )

        self.page.wait_for_timeout(2000)

        print(
            "\nTask approved successfully"
        )