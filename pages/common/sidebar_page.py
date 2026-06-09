import re

from playwright.sync_api import (
    TimeoutError
)

from pages.common.base_page import (
    BasePage
)


class SidebarPage(BasePage):

    def __init__(self, page):

        super().__init__(page)

    # ============================================
    # SELECT ORGANIZATION + ROLE
    # ============================================

    def select_organization_and_role(self):

        roles_text = self.page.get_by_text(
            "Your roles:"
        )

        try:

            # ====================================
            # WAIT FOR ROLE SCREEN
            # ====================================

            roles_text.wait_for(
                state="visible",
                timeout=3000
            )

            # ====================================
            # CLICK ROLE DROPDOWN
            # ====================================

            self.safe_click(
                roles_text
            )

            # ====================================
            # SELECT COMPANY ADMIN
            # ====================================

            company_admin = (
                self.page.locator("div")
                .filter(
                    has_text=re.compile(
                        r"^Company Admin$"
                    )
                )
                .nth(1)
            )

            company_admin.wait_for(
                state="visible",
                timeout=10000
            )

            self.safe_click(
                company_admin
            )

            # ====================================
            # CLICK CONTINUE
            # ====================================

            continue_button = self.page.get_by_role(
                "button",
                name="Continue"
            )

            self.safe_click(
                continue_button
            )

            # ====================================
            # WAIT FOR SUCCESSFUL REDIRECTION
            # ====================================

            self.page.wait_for_url(
                "https://fmn-qa.tensoract.com/",
                timeout=60000
            )

            print(
                "\nOrganization and role selected"
            )

        except TimeoutError:

            # ====================================
            # ROLE PAGE NOT SHOWN
            # ====================================

            print(
                "\nOrganization selection skipped"
            )

    # ============================================
    # OPEN INTEGRATIONS PAGE
    # ============================================

    def open_integrations_page(self):

        integrations_menu = self.page.get_by_role(
            "link",
            name="Integrations"
        )

        integrations_menu.wait_for(
            state="visible",
            timeout=60000
        )

        # ====================================
        # CLICK INTEGRATIONS
        # ====================================

        self.safe_click(
            integrations_menu
        )

        # ====================================
        # WAIT FOR PAGE NAVIGATION
        # ====================================

        self.page.wait_for_url(
            "**/s3-connections",
            timeout=60000
        )

        print(
            f"\nAfter click URL: {self.page.url}"
        )

        print(
            f"\nCurrent URL: {self.page.url}"
        )

        print(
            "\nIntegrations page opened successfully"
        )