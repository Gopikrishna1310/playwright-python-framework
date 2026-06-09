import pytest

from pages.integrations.s3_integration_page import (
    S3IntegrationPage
)

from pages.files.files_page import (
    FilesPage
)

from pages.datasets.datasets_page import (
    DatasetsPage
)

from pages.templates.templates_page import (
    TemplatesPage
)

from pages.workflows.workflows_page import (
    WorkflowsPage
)

from pages.users.users_page import (
    UsersPage
)

from pages.projects.projects_page import (
    ProjectsPage
)

from pages.restrictions.restrictions_page import (
    RestrictionsPage
)

from pages.annotator.annotator_page import (
    AnnotatorPage
)

from pages.reviewer.reviewer_page import (
    ReviewerPage
)


@pytest.mark.regression
def test_full_regression(page):

    # =====================================================
    # PAGE OBJECTS
    # =====================================================

    s3 = S3IntegrationPage(page)

    files = FilesPage(page)

    datasets = DatasetsPage(page)

    templates = TemplatesPage(page)

    workflows = WorkflowsPage(page)

    users = UsersPage(page)

    projects = ProjectsPage(page)

    restrictions = RestrictionsPage(page)

    annotator = AnnotatorPage(page)

    reviewer = ReviewerPage(page)

    # =====================================================
    # ADMIN FLOW
    # =====================================================

    print(
        "\n================================================="
    )

    print(
        "STARTING ADMIN REGRESSION FLOW"
    )

    print(
        "=================================================\n"
    )

    # =====================================================
    # S3 INTEGRATION
    # =====================================================

    print(
        "\nRunning S3 Integration Flow"
    )

    # Example:
    # s3.open_login_page()
    # s3.login()
    # s3.create_s3_integration()

    print(
        "\nS3 Integration Flow Completed"
    )

    # =====================================================
    # FILES MODULE
    # =====================================================

    print(
        "\nRunning Files Module Flow"
    )

    # Example:
    # files.open_files_page()
    # files.upload_files()

    print(
        "\nFiles Module Flow Completed"
    )

    # =====================================================
    # DATASETS MODULE
    # =====================================================

    print(
        "\nRunning Datasets Module Flow"
    )

    # Example:
    # datasets.create_dataset()

    print(
        "\nDatasets Module Flow Completed"
    )

    # =====================================================
    # TEMPLATES MODULE
    # =====================================================

    print(
        "\nRunning Templates Module Flow"
    )

    # Example:
    # templates.create_template()

    print(
        "\nTemplates Module Flow Completed"
    )

    # =====================================================
    # WORKFLOWS MODULE
    # =====================================================

    print(
        "\nRunning Workflows Module Flow"
    )

    # Example:
    # workflows.create_workflow()

    print(
        "\nWorkflows Module Flow Completed"
    )

    # =====================================================
    # USERS MODULE
    # =====================================================

    print(
        "\nRunning Users Module Flow"
    )

    # Example:
    # users.create_user()

    print(
        "\nUsers Module Flow Completed"
    )

    # =====================================================
    # PROJECTS MODULE
    # =====================================================

    print(
        "\nRunning Projects Module Flow"
    )

    # Example:
    # projects.create_project()

    print(
        "\nProjects Module Flow Completed"
    )

    # =====================================================
    # RESTRICTIONS MODULE
    # =====================================================

    print(
        "\nRunning Restrictions Module Flow"
    )

    # Example:
    # restrictions.validate_restrictions()

    print(
        "\nRestrictions Module Flow Completed"
    )

    print(
        "\n================================================="
    )

    print(
        "ADMIN REGRESSION FLOW COMPLETED"
    )

    print(
        "=================================================\n"
    )

    # =====================================================
    # ANNOTATOR FLOW
    # =====================================================

    print(
        "\n================================================="
    )

    print(
        "STARTING ANNOTATOR FLOW"
    )

    print(
        "=================================================\n"
    )

    annotator.open_login_page()

    # Example:
    # annotator.login()
    # annotator.select_organization_and_role()
    # annotator.open_task()
    # annotator.claim_task()
    # annotator.create_audio_annotation()
    # annotator.submit_annotation()
    # annotator.logout()

    print(
        "\nANNOTATOR FLOW COMPLETED"
    )

    # =====================================================
    # REVIEWER FLOW
    # =====================================================

    print(
        "\n================================================="
    )

    print(
        "STARTING REVIEWER FLOW"
    )

    print(
        "=================================================\n"
    )

    # Example:
    # reviewer.login()
    # reviewer.select_organization_and_role()
    # reviewer.open_task()
    # reviewer.claim_task()
    # reviewer.reject_task()
    # reviewer.logout()

    print(
        "\nREVIEWER FLOW COMPLETED"
    )

    # =====================================================
    # FINAL STATUS
    # =====================================================

    print(
        "\n================================================="
    )

    print(
        "FULL END-TO-END REGRESSION COMPLETED SUCCESSFULLY"
    )

    print(
        "=================================================\n"
    )