import re

from playwright.sync_api import (
    expect
)


class RestrictionsPage:

    def __init__(self, page):

        self.page = page

    # ============================================
    # OPEN WORKFLOWS PAGE
    # ============================================

    def open_workflows_page(self):

        self.page.get_by_role(
            "link",
            name="Workflows"
        ).click()

        print(
            "\nWorkflows page opened"
        )

    # ============================================
    # OPEN TEMPLATES PAGE
    # ============================================

    def open_templates_page(self):

        self.page.get_by_role(
            "link",
            name="Templates"
        ).click()

        print(
            "\nTemplates page opened"
        )

    # ============================================
    # OPEN DATASETS PAGE
    # ============================================

    def open_datasets_page(self):

        self.page.get_by_role(
            "link",
            name="Datasets"
        ).click()

        print(
            "\nDatasets page opened"
        )

    # ============================================
    # OPEN FILES PAGE
    # ============================================

    def open_files_page(self):

        self.page.get_by_role(
            "link",
            name="Files"
        ).click()

        print(
            "\nFiles page opened"
        )

    # ============================================
    # OPEN INTEGRATIONS PAGE
    # ============================================

    def open_integrations_page(self):

        self.page.get_by_role(
            "link",
            name="Integrations"
        ).click()

        print(
            "\nIntegrations page opened"
        )

    # ============================================
    # COMMON DELETE FLOW
    # ============================================

    def perform_delete_confirmation(self):

        self.page.get_by_role(
            "button",
            name="Delete"
        ).click()

        print(
            "\nDelete popup opened"
        )

        self.page.get_by_role(
            "textbox"
        ).fill(
            "DELETE"
        )

        print(
            "\nDELETE confirmation entered"
        )

        self.page.get_by_role(
            "button",
            name="Delete"
        ).click()

        print(
            "\nDelete confirmed"
        )

    # ============================================
    # VALIDATE RESTRICTION MESSAGE
    # ============================================

    def validate_restriction_message(
        self,
        message
    ):

        expect(
            self.page.get_by_text(
                message,
                exact=False
            )
        ).to_be_visible()

        print(
            f"\nRestriction message validated:\n{message}"
        )

    # ============================================
    # CLOSE POPUP
    # ============================================

    def close_popup(self):

        self.page.locator(
            "button"
        ).filter(
            has_text=""
        ).last.click()

        self.page.wait_for_timeout(
            2000
        )

        print(
            "\nPopup closed"
        )

    # ============================================
    # TC_09_01
    # DELETE WORKFLOW RESTRICTION
    # ============================================

    def attempt_delete_workflow(
        self,
        workflow_name
    ):

        self.page.get_by_role(
            "row",
            name=re.compile(
                workflow_name
            )
        ).get_by_role(
            "checkbox"
        ).check()

        print(
            f"\nWorkflow selected:\n{workflow_name}"
        )

        self.perform_delete_confirmation()

    # ============================================
    # TC_09_02
    # DELETE TEMPLATE RESTRICTION
    # ============================================

    def attempt_delete_template(
        self,
        template_name
    ):

        self.page.get_by_role(
            "row",
            name=re.compile(
                template_name
            )
        ).get_by_role(
            "checkbox"
        ).check()

        print(
            f"\nTemplate selected:\n{template_name}"
        )

        self.perform_delete_confirmation()

    # ============================================
    # TC_09_03
    # DELETE DATASET RESTRICTION
    # ============================================

    def attempt_delete_dataset(
        self,
        dataset_name
    ):

        self.page.get_by_role(
            "row",
            name=re.compile(
                dataset_name
            )
        ).get_by_role(
            "checkbox"
        ).check()

        print(
            f"\nDataset selected:\n{dataset_name}"
        )

        self.perform_delete_confirmation()

    # ============================================
    # OPEN DATASET
    # ============================================

    def open_dataset(
        self,
        dataset_name
    ):

        self.page.get_by_text(
            dataset_name
        ).click()

        print(
            f"\nDataset opened:\n{dataset_name}"
        )

    # ============================================
    # TC_09_04
    # DELETE DATASET FILES RESTRICTION
    # ============================================

    def attempt_delete_dataset_files(
        self,
        file_names
    ):

        for file_name in file_names:

            self.page.get_by_role(
                "row",
                name=re.compile(
                    file_name
                )
            ).get_by_role(
                "checkbox"
            ).check()

            print(
                f"\nDataset file selected:\n{file_name}"
            )

        self.perform_delete_confirmation()

    # ============================================
    # TC_09_05
    # DELETE FILES PAGE FILES RESTRICTION
    # ============================================

    def attempt_delete_files(
        self,
        file_names
    ):

        for file_name in file_names:

            self.page.get_by_role(
                "row",
                name=re.compile(
                    file_name
                )
            ).get_by_role(
                "checkbox"
            ).check()

            print(
                f"\nFile selected:\n{file_name}"
            )

        self.perform_delete_confirmation()

    # ============================================
    # TC_09_06
    # DELETE INTEGRATION RESTRICTION
    # ============================================

    def attempt_delete_integration(
        self,
        integration_name
    ):

        self.page.get_by_role(
            "row",
            name=re.compile(
                integration_name
            )
        ).get_by_role(
            "checkbox"
        ).check()

        print(
            f"\nIntegration selected:\n{integration_name}"
        )

        self.perform_delete_confirmation()