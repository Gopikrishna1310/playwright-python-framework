import logging
import pytest

from pages.common.login_page import LoginPage
from pages.common.sidebar_page import SidebarPage
from pages.integrations.s3_integration_page import S3IntegrationPage
from pages.files.files_page import FilesPage
from pages.datasets.datasets_page import DatasetsPage
from pages.templates.templates_page import TemplatesPage
from pages.workflows.workflows_page import WorkflowsPage
from pages.users.users_page import UsersPage
from pages.projects.projects_page import ProjectsPage
from pages.restrictions.restrictions_page import RestrictionsPage
from pages.annotator.annotator_page import AnnotatorPage
from pages.reviewer.reviewer_page import ReviewerPage

from config.credentials import (
    TOOL_EMAIL,
    TOOL_PASSWORD,
    ANNOTATOR_EMAIL,
    ANNOTATOR_PASSWORD,
    REVIEWER_EMAIL,
    REVIEWER_PASSWORD,
    AWS_ACCOUNT,
    AWS_USERNAME,
    AWS_PASSWORD,
)

from config.test_data import (
    INTEGRATION_TITLE,
    S3_BUCKET_NAME,
    ROLE_NAME,
)

from pages.aws.aws_login_page import AWSLoginPage
from pages.aws.aws_iam_page import AWSIAMPage
from pages.aws.aws_role_page import AWSRolePage
from pages.aws.aws_s3_page import AWSS3Page

logger = logging.getLogger(__name__)


@pytest.mark.regression
def test_full_regression(page):

    # =========================================================================
    # STEP 1: ADMIN LOGIN
    # =========================================================================

    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(TOOL_EMAIL, TOOL_PASSWORD)
    # login() already handles org/role selection internally
    logger.info("Admin login completed")

    # =========================================================================
    # STEP 2: INTEGRATIONS — full S3 setup
    # =========================================================================

    s3_page = S3IntegrationPage(page)
    sidebar_page = SidebarPage(page)
    sidebar_page.open_integrations_page()

    s3_page.open_new_integration_popup()
    s3_page.verify_popup_opened()
    s3_page.enter_basic_details(INTEGRATION_TITLE, S3_BUCKET_NAME)
    s3_page.open_step_2()
    s3_page.verify_policy_json_visible()
    policy_json = s3_page.get_policy_json()
    assert policy_json.startswith("{")

    aws_tab = page.context.new_page()

    aws_login = AWSLoginPage(aws_tab)
    aws_login.open_aws_login_page()
    aws_login.login_to_aws(AWS_ACCOUNT, AWS_USERNAME, AWS_PASSWORD)

    iam = AWSIAMPage(aws_tab)
    iam.open_iam_console()
    iam.open_policies_page()
    iam.search_policy(S3_BUCKET_NAME)
    iam.open_policy(S3_BUCKET_NAME)
    iam.click_edit_policy()
    iam.replace_policy_json(policy_json)
    iam.save_policy()

    s3_page.open_step_3()
    s3_page.verify_account_external_id_fields_visible()
    account_id  = s3_page.get_account_id()
    external_id = s3_page.get_external_id()
    assert account_id != ""
    assert external_id != ""

    role_page = AWSRolePage(aws_tab)
    role_page.open_roles_page()
    role_page.click_create_role()
    role_page.select_aws_account()
    role_page.select_another_aws_account()
    role_page.enter_account_id(account_id)
    role_page.enable_external_id()
    role_page.enter_external_id(external_id)
    role_page.go_to_permissions_page()
    role_page.attach_policy(S3_BUCKET_NAME)
    role_page.enter_role_name(ROLE_NAME)
    role_page.create_role()
    role_page.open_created_role(ROLE_NAME)
    role_page.copy_role_arn()

    s3_page.switch_to_page(page)
    s3_page.paste_role_arn()
    s3_page.open_step_4()
    s3_page.verify_cors_json_visible()
    cors_json = s3_page.copy_cors_json()
    assert cors_json.startswith("[")

    s3_aws = AWSS3Page(aws_tab)
    s3_aws.open_s3_console()
    s3_aws.search_bucket(S3_BUCKET_NAME)
    s3_aws.open_bucket(S3_BUCKET_NAME)
    s3_aws.open_permissions_tab()
    s3_aws.click_edit_cors()
    s3_aws.replace_cors_json(cors_json)
    s3_aws.save_changes()

    s3_page.switch_to_page(page)
    s3_page.click_create_integration()
    s3_page.verify_integration_created()
    s3_page.verify_integration_visible_in_list(INTEGRATION_TITLE)
    logger.info("Integrations module completed")

    # =========================================================================
    # STEP 3: FILES — upload audio files
    # =========================================================================

    files_page = FilesPage(page)
    files_page.open_files_page()
    files_page.verify_files_page_opened()

    files_page.open_upload_files_popup()
    files_page.upload_single_file("test_data/files/audio/audio 1.aac")
    files_page.click_upload_button()
    files_page.verify_upload_success()
    files_page.verify_file_visible("audio 1.aac")

    files_page.open_upload_files_popup()
    files_page.upload_multiple_files([
        "test_data/files/audio/audio 2.flac",
        "test_data/files/audio/audio 3.mp3",
        "test_data/files/audio/audio 4.wav",
    ])
    files_page.click_upload_button()
    files_page.verify_upload_success()
    for f in ["audio 2.flac", "audio 3.mp3", "audio 4.wav"]:
        files_page.verify_file_visible(f)

    logger.info("Files module completed")

    # =========================================================================
    # STEP 4: DATASETS — create Test 3 and Test audio 2
    # =========================================================================

    datasets_page = DatasetsPage(page)
    datasets_page.open_datasets_page()
    datasets_page.verify_datasets_page_opened()

    for name, dtype, desc in [
        ("Test 3",       "Audio", "Description"),
        ("Test audio 2", "Audio", ""),
    ]:
        datasets_page.create_dataset(dataset_name=name, dataset_type=dtype, description=desc)
        datasets_page.verify_dataset_visible(name)

    datasets_page.open_dataset("Test 3")
    datasets_page.open_add_files_popup()
    for f in ["Copy - Copy.mp3", "Copy - Copy.wav", "audio 4.wav", "audio 1.aac"]:
        datasets_page.select_dataset_file(f)
    datasets_page.click_add_files_button()
    for f in ["Copy - Copy.mp3", "Copy - Copy.wav", "audio 4.wav", "audio 1.aac"]:
        datasets_page.verify_file_in_dataset(f)

    datasets_page.open_datasets_page()
    datasets_page.open_dataset("Test audio 2")
    datasets_page.open_add_files_popup()
    for f in ["audio 4.wav", "Copy - Copy.wav"]:
        datasets_page.select_dataset_file(f)
    datasets_page.click_add_files_button()
    for f in ["audio 4.wav", "Copy - Copy.wav"]:
        datasets_page.verify_file_in_dataset(f)

    logger.info("Datasets module completed")

    # =========================================================================
    # STEP 5: TEMPLATES — upload Test template - 1
    # =========================================================================

    templates_page = TemplatesPage(page)
    templates_page.open_templates_page()
    templates_page.verify_templates_page_opened()
    templates_page.upload_template(
        "Test template - 1",
        "test_data/files/template/Updated Audio template.zip"
    )
    templates_page.verify_template_visible("Test template - 1")
    logger.info("Templates module completed")

    # =========================================================================
    # STEP 6: WORKFLOWS — create Testing workflow 1
    # =========================================================================

    workflows_page = WorkflowsPage(page)
    workflows_page.open_workflows_page()
    workflows_page.verify_workflows_page_opened()
    workflows_page.create_workflow("Testing workflow 1", "Description")
    workflows_page.create_nodes()
    workflows_page.verify_node_on_canvas(".react-flow__node-annotate", "Annotate")
    workflows_page.select_template()
    workflows_page.connect_reject_to_annotate()
    workflows_page.verify_edge_connected()
    workflows_page.save_workflow()
    workflows_page.open_workflows_page()
    workflows_page.verify_workflow_visible("Testing workflow 1")
    logger.info("Workflows module completed")

    # =========================================================================
    # STEP 7: USERS — create annotator and reviewer users
    # =========================================================================

    users_page = UsersPage(page)
    users_page.open_users_page()
    users_page.verify_users_page_opened()

    users_page.create_user(
        full_name="User 1",
        email="user1@objectways.com",
        password="User123!",
        roles=["Annotator"]
    )
    users_page.verify_user_in_list("user1@objectways.com")
    logger.info("Users module completed")

    # =========================================================================
    # STEP 8: PROJECTS — create project and configure
    # =========================================================================

    projects_page = ProjectsPage(page)
    projects_page.open_projects_page()
    projects_page.verify_projects_page_opened()

    projects_page.create_project(
        project_name="Test project 1",
        datasets=["Test 3"],
        workflow="Testing workflow 1",
        description="Description"
    )
    projects_page.verify_project_in_list("Test project 1")

    projects_page.open_project("Test project 1")
    projects_page.verify_tasks_tab_open()

    projects_page.add_dataset_to_project("Test audio 2")
    projects_page.verify_dataset_in_project("Test audio 2")

    projects_page.add_project_users(
        role="ANNOTATOR",
        users=["Objectways Annotator 1"]
    )
    projects_page.verify_user_in_teams("Objectways Annotator 1")

    projects_page.add_project_users(
        role="REVIEWER",
        users=["Objectways Reviewer"]
    )
    projects_page.verify_user_in_teams("Objectways Reviewer")
    logger.info("Projects module completed")

    # =========================================================================
    # STEP 9: RESTRICTIONS — validate protected items cannot be deleted
    # =========================================================================

    restrictions_page = RestrictionsPage(page)

    restrictions_page.open_workflows_page()
    restrictions_page.verify_page_url("/workflows")
    restrictions_page.attempt_delete_workflow("Testing workflow 1")
    restrictions_page.verify_restriction_message("Failed Deleted Workflow")
    restrictions_page.close_popup()
    restrictions_page.verify_item_still_in_list("Testing workflow 1")

    restrictions_page.open_templates_page()
    restrictions_page.verify_page_url("/templates")
    restrictions_page.attempt_delete_template("Test template - 1")
    restrictions_page.verify_restriction_message("Failed Deleted Template")
    restrictions_page.close_popup()
    restrictions_page.verify_item_still_in_list("Test template - 1")

    restrictions_page.open_datasets_page()
    restrictions_page.verify_page_url("/datasets")
    restrictions_page.attempt_delete_dataset("Test 3")
    restrictions_page.verify_restriction_message("Failed Deleted Dataset")
    restrictions_page.close_popup()
    restrictions_page.verify_item_still_in_list("Test 3")

    restrictions_page.open_dataset("Test 3")
    restrictions_page.attempt_delete_dataset_files(["Copy - Copy.wav", "audio 4.wav"])
    restrictions_page.verify_restriction_message("Failed Detached Files")
    restrictions_page.close_popup()
    restrictions_page.verify_files_still_in_list(["Copy - Copy.wav", "audio 4.wav"])

    restrictions_page.open_files_page()
    restrictions_page.verify_page_url("/files")
    restrictions_page.attempt_delete_files(["Copy - Copy.wav", "audio 4.wav"])
    restrictions_page.verify_restriction_message("Failed Deletions")
    restrictions_page.close_popup()
    restrictions_page.verify_files_still_in_list(["Copy - Copy.wav", "audio 4.wav"])

    restrictions_page.open_integrations_page()
    restrictions_page.verify_page_url("/s3-connections")
    restrictions_page.attempt_delete_integration(INTEGRATION_TITLE)
    restrictions_page.verify_restriction_message("Failed Deleted Integration")
    restrictions_page.close_popup()
    restrictions_page.verify_item_still_in_list(INTEGRATION_TITLE)

    logger.info("Restrictions module completed")

    # =========================================================================
    # STEP 10: ADMIN LOGOUT
    # =========================================================================

    # Navigate to login page directly — cleanest way to end admin session
    # before switching to annotator credentials
    page.goto(f"{page.url.split('/')[0]}//{page.url.split('/')[2]}/login")
    logger.info("Admin session ended")

    # =========================================================================
    # STEP 11: ANNOTATOR — login → claim → annotate → submit → logout
    # =========================================================================

    annotator = AnnotatorPage(page)
    annotator.open_login_page()
    annotator.login(ANNOTATOR_EMAIL, ANNOTATOR_PASSWORD)
    annotator.select_organization_and_role()
    annotator.validate_annotator_login()
    logger.info("Annotator login completed")

    annotator.open_task("Test project 1")
    annotator.claim_task()
    annotator.create_audio_annotation("Test transcription")
    annotator.submit_annotation()
    logger.info("Annotator task submitted")

    annotator.logout()
    logger.info("Annotator logout completed")

    # =========================================================================
    # STEP 12: REVIEWER — login → claim → reject → logout
    # =========================================================================

    reviewer = ReviewerPage(page)
    reviewer.open_login_page()
    reviewer.login(REVIEWER_EMAIL, REVIEWER_PASSWORD)
    reviewer.select_organization_and_role()
    reviewer.validate_reviewer_login()
    logger.info("Reviewer login completed")

    reviewer.open_task("Test project 1")
    reviewer.claim_task()
    reviewer.reject_task("Need correction in annotation")
    logger.info("Reviewer rejected task")

    reviewer.open_profile_menu()
    reviewer.logout()
    logger.info("Reviewer logout completed")

    # =========================================================================
    # STEP 13: ANNOTATOR — login → pick rejected task → resubmit → logout
    # =========================================================================

    annotator.open_login_page()
    annotator.login(ANNOTATOR_EMAIL, ANNOTATOR_PASSWORD)
    annotator.select_organization_and_role()
    logger.info("Annotator re-login completed")

    annotator.open_task("Test project 1")

    # Rejection feedback popup auto-opens — close it before resubmitting
    page.get_by_role("button", name="Close").click()
    logger.info("Rejection popup closed")

    annotator.wait_for_template_load()
    annotator.submit_annotation()
    logger.info("Annotator resubmitted task")

    annotator.logout()
    logger.info("Annotator logout completed")

    # =========================================================================
    # STEP 14: REVIEWER — login → pick resubmitted task → approve → logout
    # =========================================================================

    reviewer.open_login_page()
    reviewer.login(REVIEWER_EMAIL, REVIEWER_PASSWORD)
    reviewer.select_organization_and_role()
    logger.info("Reviewer re-login completed")

    reviewer.open_task("Test project 1")
    reviewer.approve_task()
    logger.info("Reviewer approved task")

    reviewer.open_profile_menu()
    reviewer.logout()
    logger.info("Reviewer final logout completed")

    logger.info("FULL END-TO-END REGRESSION COMPLETED SUCCESSFULLY")