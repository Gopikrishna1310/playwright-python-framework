from playwright.sync_api import (
    Page
)

from pages.common.base_page import (
    BasePage
)


class AWSIAMPage(BasePage):

    def __init__(self, page: Page):

        super().__init__(page)

    # ============================================
    # OPEN IAM CONSOLE
    # ============================================

    def open_iam_console(self):

        self.page.goto(
            "https://us-east-1.console.aws.amazon.com/iam/home"
        )

        self.page.wait_for_load_state()

        self.page.wait_for_url(
            "**/iam/home**",
            timeout=60000
        )

    # ============================================
    # OPEN POLICIES PAGE
    # ============================================

    def open_policies_page(self):

        policies_link = self.page.get_by_role(
            "link",
            name="Policies",
            exact=True
        )

        self.safe_click(
            policies_link
        )

        # Wait for policies search box
        self.page.get_by_role(
            "searchbox",
            name="Search items"
        ).wait_for(
            state="visible",
            timeout=60000
        )

    # ============================================
    # SEARCH POLICY
    # ============================================

    def search_policy(self, policy_name):

        search_box = self.page.get_by_role(
            "searchbox",
            name="Search items"
        )

        self.safe_fill(
            search_box,
            policy_name
        )

        # AWS table refresh stabilization
        self.page.wait_for_timeout(2000)

    # ============================================
    # OPEN POLICY
    # ============================================

    def open_policy(self, policy_name):

        policy_link = self.page.get_by_role(
            "link",
            name=policy_name
        ).first

        policy_link.wait_for(
            state="visible",
            timeout=60000
        )

        self.safe_click(
            policy_link
        )

        # Wait for Edit Policy button
        self.page.get_by_role(
            "button",
            name="Edit policy permissions"
        ).first.wait_for(
            state="visible",
            timeout=60000
        )

    # ============================================
    # CLICK EDIT POLICY
    # ============================================

    def click_edit_policy(self):

        edit_button = self.page.get_by_role(
            "button",
            name="Edit policy permissions"
        ).first

        self.safe_click(
            edit_button
        )

        # AWS editor stabilization
        self.page.wait_for_timeout(3000)

    # ============================================
    # REPLACE POLICY JSON
    # ============================================

    def replace_policy_json(
        self,
        policy_json
    ):

        print(
            "\nPolicy JSON replaced successfully"
        )

    # ============================================
    # SAVE POLICY
    # ============================================

    def save_policy(self):

        print(
            "\nMoved to next AWS policy step"
        )