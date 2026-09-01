import allure
import pytest
from actions.action_factory import ActionFactory
from tests.workflows.test_data_inputs import test_data_inputs

@pytest.fixture
def before_each(page):
    action_factory = ActionFactory(page)
    url = action_factory.helpers.fetch_dotenv("Execution_url")
    email = action_factory.helpers.fetch_dotenv("company_Username")
    password = action_factory.helpers.fetch_dotenv("company_Password")
    company_Name = action_factory.helpers.fetch_dotenv("company_Name")
    diff_email = action_factory.helpers.fetch_dotenv("different_email_for_otp")
    diff_email_password = action_factory.helpers.fetch_dotenv("different_email_for_otp_password")
    
    # Login & Setup
    action_factory.login_actions.perform_login(url=url, email=email, password=password)
    action_factory.login_actions.use_different_email_OTP(diff_email, diff_email_password)
    action_factory.login_actions.select_organization(company_Name, "Company Admin")
    return action_factory

@allure.feature("Workflows")
@allure.story("TC_20: Start -> Annotate 1 -> Annotate 2 Consensus -> Review -> Complete (Delete Linked)")
@allure.title("Verify attempting to delete a TC_20 workflow linked to an active project is blocked")
def test_tc20_delete_wf_start_ann1_ann2_consensus_rev_complete(before_each):
    status = "Fail"
    message = ""
    try:
        action_factory = before_each
        dataset_name = test_data_inputs.common_dataset_name
        template_name = test_data_inputs.common_template_name_A
        workflow_name = test_data_inputs.tc20_delete_workflow_name
        project_name = test_data_inputs.tc20_project_name
        description = test_data_inputs.description
        template_file = test_data_inputs.valid_template_file
        dataset_files = test_data_inputs.dataset_files
        nodes_list = ["Start", "Annotate", "Annotate", "Review", "Complete"]

        # Create Dataset
        action_factory.datasets_actions.click_datasets_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.create_dataset(dataset_name=dataset_name, dataset_type_name="Audio", description=description)
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.datasets_page.click_dataset_file_name(dataset_name))
        action_factory.ui_utils.smart_wait()
        action_factory.datasets_actions.upload_files_with_uploadBtn(*dataset_files)
        action_factory.common_actions.validate_toast_msg("1 file added")
        action_factory.ui_utils.smart_wait()

        # Create Template
        action_factory.templates_actions.click_templates_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.templates_actions.upload_new_template(template_name=template_name, description=description)
        action_factory.templates_actions.upload_template_files(template_file)
        action_factory.templates_actions.validate_template_toast_msg("Successfully created Templates")
        action_factory.ui_utils.smart_wait()

        # Create Workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.workflows_actions.create_workflow(workflow_name=workflow_name, description=description)
        action_factory.ui_utils.smart_wait()
        for node in nodes_list:
            action_factory.workflows_actions.click_nodes(node_name=node)
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.fit_view)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name, position=0)
        action_factory.workflows_actions.apply_template_to_annotate(template_name=template_name, position=1)
        action_factory.ui_utils.smart_wait()

        action_factory.workflows_actions.required_annotator("2")
        action_factory.ui_utils.smart_wait()

        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="annotate", node_index1=2, position1="right", index1=2,
            node_Name2="annotate", node_index2=1, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()

        action_factory.workflows_actions.nodes_connection_flow(
            node_Name1="review", node_index1=1, position1="right", index1=2,
            node_Name2="annotate", node_index2=2, position2="left", index2=1
        )
        action_factory.ui_utils.smart_wait()
        action_factory.ui_utils.click_element(action_factory.page_factory.workflows_page.save_btn)
        action_factory.ui_utils.smart_wait()

        # Create Project linking dataset and workflow
        action_factory.projects_actions.click_project_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.projects_actions.create_project(
            project_name=project_name,
            dataset_name=dataset_name,
            workflow_name=workflow_name,
            description=description
        )
        action_factory.ui_utils.smart_wait()

        # Attempt to delete linked workflow
        action_factory.workflows_actions.click_workflows_menu()
        action_factory.ui_utils.smart_wait()
        action_factory.workflows_actions.delete_workflow(workflow_name)
        action_factory.ui_utils.smart_wait()

        error_visible = action_factory.ui_utils.is_element_visible(action_factory.page_factory.workflows_page.workflow_delete_failed_popup)
        remaining_workflows = action_factory.ui_utils.grab_text_from_all(action_factory.page_factory.workflows_page.workflow_names_list)

        if error_visible and workflow_name in remaining_workflows:
            status = "Pass"
            message = f"Deletion of linked workflow '{workflow_name}' was blocked as expected."
            action_factory.helpers.attach_screenshot(name="TC20PreventDeleteLinkedWorkflowPass")
            action_factory.helpers.attach_allure(name="TC_10 Delete Linked Workflow", text=message)
            assert True, message
        else:
            status = "Fail"
            message = f"Linked workflow '{workflow_name}' was unexpectedly deleted."
            action_factory.helpers.attach_screenshot(name="TC10PreventDeleteLinkedWorkflowFailed")
            action_factory.helpers.attach_allure(name="TC_10 Delete Linked Workflow", text=message)
            assert False, message

    except Exception as e:
        status = "Fail"
        message = str(e)
        action_factory.helpers.handle_failure(message=message)
        raise

    finally:
        action_factory.helpers.write_test_results(
            status=status,
            message=message
        )
