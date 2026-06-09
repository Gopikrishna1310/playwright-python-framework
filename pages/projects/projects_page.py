import re

from playwright.sync_api import (
    expect
)


class ProjectsPage:

    def __init__(self, page):

        self.page = page

    # ============================================
    # OPEN PROJECTS PAGE
    # ============================================

    def open_projects_page(self):

        self.page.get_by_role(
            "link",
            name="Projects"
        ).click()

        print(
            "\nProjects page opened"
        )

    # ============================================
    # VALIDATE PROJECTS PAGE
    # ============================================

    def validate_projects_page_opened(self):

        expect(
            self.page.get_by_role(
                "heading",
                name="Projects"
            )
        ).to_be_visible()

        print(
            "\nProjects page validation successful"
        )

    # ============================================
    # CREATE PROJECT
    # ============================================

    def create_project(
        self,
        project_name,
        datasets,
        workflow,
        description=""
    ):

        self.page.get_by_role(
            "button",
            name="Create Project"
        ).click()

        print(
            "\nCreate Project popup opened"
        )

        # ============================================
        # PROJECT NAME
        # ============================================

        self.page.get_by_role(
            "textbox",
            name="Enter Project Name"
        ).fill(
            project_name
        )

        print(
            f"\nProject name entered:\n{project_name}"
        )

        # ============================================
        # SELECT DATASETS
        # ============================================

        self.page.get_by_role(
            "button",
            name="Select Datasets"
        ).click()

        self.page.wait_for_timeout(2000)

        for dataset_name in datasets:

            dataset_locator = self.page.locator(
                "div"
            ).filter(
                has_text=re.compile(
                    rf"^{dataset_name}$"
                )
            )

            dataset_locator.locator(
                "input[type='checkbox']"
            ).check()

            print(
                f"\nDataset selected:\n{dataset_name}"
            )

            self.page.wait_for_timeout(1000)

        self.page.get_by_role(
            "button",
            name=re.compile(
                r"dataset\(s\) selected"
            )
        ).click()

        # ============================================
        # SELECT WORKFLOW
        # ============================================

        self.page.get_by_role(
            "button",
            name="Select Workflow"
        ).click()

        self.page.wait_for_timeout(1000)

        self.page.locator(
            "div"
        ).filter(
            has_text=re.compile(
                rf"^{workflow}$"
            )
        ).click()

        print(
            f"\nWorkflow selected:\n{workflow}"
        )

        # ============================================
        # DESCRIPTION
        # ============================================

        if description:

            self.page.get_by_role(
                "textbox",
                name="Enter Project Description"
            ).fill(
                description
            )

            print(
                f"\nProject description entered:\n{description}"
            )

        # ============================================
        # CREATE PROJECT
        # ============================================

        self.page.get_by_role(
            "button",
            name="Create Project"
        ).click()

        print(
            "\nCreate Project button clicked"
        )

        self.page.wait_for_timeout(3000)

        # ============================================
        # VALIDATE PROJECT
        # ============================================

        expect(
            self.page.get_by_role(
                "row",
                name=re.compile(project_name)
            )
        ).to_be_visible()

        print(
            f"\nProject validated:\n{project_name}"
        )

    # ============================================
    # OPEN PROJECT
    # ============================================

    def open_project(
        self,
        project_name
    ):

        self.page.get_by_text(
            project_name
        ).click()

        print(
            f"\nProject opened:\n{project_name}"
        )

    # ============================================
    # VALIDATE TASKS PAGE
    # ============================================

    def validate_tasks_page(self):

        expect(
            self.page.get_by_role(
                "button",
                name="Export"
            )
        ).to_be_visible()

        expect(
            self.page.get_by_role(
                "button",
                name="Reset"
            )
        ).to_be_visible()

        expect(
            self.page.get_by_role(
                "textbox",
                name="search"
            ).first
        ).to_be_visible()

        print(
            "\nTasks page controls validated"
        )

    # ============================================
    # EXPORT PROJECT DATA
    # ============================================

    def export_project_data(self):

        with self.page.expect_download():

            self.page.get_by_role(
                "button",
                name="Export"
            ).click()

        print(
            "\nProject export completed"
        )

    # ============================================
    # RESET TASKS
    # ============================================

    def reset_tasks(
        self,
        file_names
    ):

        for file_name in file_names:

            self.page.get_by_role(
                "row",
                name=re.compile(file_name)
            ).get_by_role(
                "checkbox"
            ).check()

            print(
                f"\nTask selected:\n{file_name}"
            )

        self.page.get_by_role(
            "button",
            name="Reset"
        ).click()

        self.page.get_by_role(
            "textbox"
        ).fill(
            "RESET"
        )

        self.page.get_by_role(
            "button",
            name="Reset"
        ).click()

        print(
            "\nTasks reset completed"
        )

        # ============================================
        # CLOSE RESET SUMMARY POPUP
        # ============================================

        self.page.locator(
            "div[role='dialog'] button"
        ).last.click()

        print(
            "\nReset summary popup closed"
        )

        self.page.wait_for_timeout(2000)

    # ============================================
    # ADD DATASET TO PROJECT
    # ============================================

    def add_dataset_to_project(
        self,
        dataset_name
    ):

        self.page.get_by_role(
            "tab",
            name="Datasets"
        ).click()

        self.page.get_by_role(
            "button",
            name="Add"
        ).click()

        self.page.get_by_role(
            "row",
            name=re.compile(dataset_name)
        ).get_by_role(
            "checkbox"
        ).check()

        self.page.get_by_role(
            "button",
            name="Add/Sync"
        ).click()

        print(
            f"\nDataset added to project:\n{dataset_name}"
        )

    # ============================================
    # ADD PROJECT USERS
    # ============================================

    def add_project_users(
        self,
        role,
        users
    ):

        self.page.get_by_role(
            "tab",
            name="Teams"
        ).click()

        self.page.get_by_role(
            "button",
            name="Add Users"
        ).click()

        self.page.wait_for_timeout(1000)

        if role != "ANNOTATOR":

            self.page.get_by_role(
                "combobox"
            ).select_option(
                role
            )

        for user in users:

            self.page.get_by_role(
                "row",
                name=re.compile(user)
            ).get_by_role(
                "checkbox"
            ).check()

            print(
                f"\nUser selected:\n{user}"
            )

        self.page.get_by_role(
            "button",
            name="Add"
        ).click()

        print(
            f"\n{role} users added successfully"
        )

    # ============================================
    # REMOVE PROJECT USERS
    # ============================================

    def remove_project_users(
            self,
            users
    ):

        # ========================================
        # OPEN TEAMS TAB
        # ========================================

        self.page.get_by_role(
            "tab",
            name="Teams"
        ).click()

        self.page.wait_for_timeout(1000)

        # ========================================
        # SELECT USERS
        # ========================================

        for user in users:
            user_row = self.page.get_by_role(
                "row",
                name=re.compile(user)
            )

            checkbox = user_row.get_by_role(
                "checkbox"
            )

            checkbox.check()

            print(
                f"\nUser selected for remove:\n{user}"
            )

        # ========================================
        # WAIT FOR UI TO UPDATE
        # ========================================

        self.page.wait_for_timeout(2000)

        # ========================================
        # REMOVE BUTTON
        # ========================================

        remove_button = self.page.get_by_role(
            "button",
            name=re.compile(
                r"Remove Selected"
            )
        )

        expect(
            remove_button
        ).to_be_enabled()

        remove_button.click()

        print(
            "\nRemove button clicked"
        )

        # ========================================
        # DELETE CONFIRMATION
        # ========================================

        self.page.get_by_role(
            "textbox"
        ).fill(
            "DELETE"
        )

        self.page.get_by_role(
            "button",
            name="Remove"
        ).click()

        print(
            "\nProject users removed successfully"
        )

    # ============================================
    # DELETE PROJECT
    # ============================================

    def delete_project(
        self,
        project_name
    ):

        self.page.get_by_role(
            "row",
            name=re.compile(project_name)
        ).get_by_role(
            "checkbox"
        ).check()

        print(
            f"\nProject selected for delete:\n{project_name}"
        )

        self.page.get_by_role(
            "button",
            name="Delete"
        ).click()

        self.page.get_by_role(
            "textbox"
        ).fill(
            "DELETE"
        )

        self.page.get_by_role(
            "button",
            name="Delete"
        ).click()

        print(
            f"\nProject deleted:\n{project_name}"
        )

        # ============================================
        # CLOSE DELETE SUMMARY POPUP
        # ============================================

        self.page.locator(
            "div[role='dialog'] button"
        ).last.click()

        print(
            "\nDelete summary popup closed"
        )

        self.page.wait_for_timeout(2000)